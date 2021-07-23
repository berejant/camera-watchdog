from typing import Optional
from requests import Session
from requests.exceptions import RequestException
from decouple import config
import cv2
import numpy as np

session = Session()
api_uri = config("NOMEROFF_API_URI", "")


def detect(img: np.ndarray) -> Optional[str]:
    if api_uri == "":
        return None

    image_bytes = cv2.imencode('.jpg', img)[1].tobytes()

    try:
        number = session.post(url=api_uri, data=image_bytes, timeout=10).content.strip().decode("utf-8")
        return number if number else None

    except RequestException:
        print('Failed to detect number')
        return None
