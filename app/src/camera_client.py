from onvif import ONVIFCamera
import onvif
from requests import Session, Request
from requests.auth import HTTPDigestAuth
from requests.exceptions import RequestException
from urllib.parse import urlparse, quote
import numpy as np
import cv2
from typing import Optional
import os

class CameraClient:
    snapshot_request: Request
    snapshot_session: Session
    stream_uri: str

    def __init__(self, ip, port, username, password):
        wsdl_dir = os.path.abspath(list(onvif.__path__)[0] + '/../../site-packages/wsdl')
        onvif_client = ONVIFCamera(ip, port, username, password, wsdl_dir)

        media_service = onvif_client.create_media_service()
        profiles = media_service.GetProfiles()
        token = profiles[0].token

        stream_uri_request = media_service.create_type('GetStreamUri')
        stream_uri_request.ProfileToken = token
        stream_uri_request.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
        stream_uri_response = media_service.GetStreamUri(stream_uri_request)
        stream_uri = urlparse(stream_uri_response.Uri)
        self.stream_uri = stream_uri.scheme + '://' + quote(username) + ':' + quote(password) + '@' \
                          + stream_uri.netloc + stream_uri.path + \
                          ('' if not stream_uri.query else '?' + stream_uri.query)

        snapshot_uri_request = media_service.create_type('GetSnapshotUri')
        snapshot_uri_request.ProfileToken = token
        snapshot_uri_response = media_service.GetSnapshotUri(snapshot_uri_request)
        snapshot_uri = snapshot_uri_response.Uri

        self.snapshot_request = Request('GET', snapshot_uri, auth=HTTPDigestAuth(username, password))
        self.snapshot_session = Session()

    def get_snapshot(self) -> Optional[bytes]:
        try:
            return self.snapshot_session.send(self.snapshot_request.prepare(), timeout=1).content
        except RequestException:
            print('Failed to get snapshot')
            return None

    def get_high_resolution_snapshot(self) -> Optional[np.ndarray]:
        cap = cv2.VideoCapture(self.stream_uri)
        if cap.isOpened():
            _, frame = cap.read()
            cap.release()  # releasing camera immediately after capturing picture
            if _ and frame is not None:
                return frame

        print('Failed to get high resolution snapshot')
        return None