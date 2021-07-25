#!/usr/bin/env python3
from decouple import config
import telegram
from src.storage import Storage
from src.camera_client import CameraClient
from src.watchdog import Watchdog
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

camera_client = CameraClient(config('CAMERA_IP'), config('CAMERA_PORT', 80),
                      config('CAMERA_USERNAME'), config('CAMERA_PASSWORD'))
telegram_bot = telegram.Bot(token=config('TELEGRAM_TOKEN'))
storage = Storage(config('STORAGE_DIR'))
watchdog = Watchdog(storage=storage, camera_client=camera_client, telegram_bot=telegram_bot, telegram_chat_id=config('TELEGRAM_CHAT_ID'))


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', '0')
        self.end_headers()

        if self.path == '/webhook':
            watchdog.pull_snapshot()
        elif self.path == '/send_snapshot':
            watchdog.pull_snapshot()
            watchdog.send_snapshot(disable_notification=True)

    def do_POST(self):
        if self.path == '/send_snapshot':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            print(post_data)
            post_data = parse_qs(post_data)
            text = post_data["text"][0] if "text" in post_data else None
            watchdog.send_snapshot(text=text)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Content-Length', '0')
            self.end_headers()

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
