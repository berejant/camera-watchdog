#!/usr/bin/env python3
from src.config import config
from src.storage import Storage
from src.watchdog import Watchdog
from requests import Request
from requests.auth import HTTPDigestAuth
from http.server import HTTPServer, BaseHTTPRequestHandler

snapshot_request = Request('GET', config['SNAPSHOT_URL'], auth=HTTPDigestAuth(config['SNAPSHOT_AUTH_LOGIN'], config['SNAPSHOT_AUTH_PASSWORD']))
storage = Storage(config['STORAGE_DIR'])
watchdog = Watchdog(storage=storage, snapshot_request=snapshot_request)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        watchdog.pull_snapshot()

httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()

