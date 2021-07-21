#!/usr/bin/env python3
from decouple import config
from src.storage import Storage
from src.watchdog import Watchdog
from requests import Request
from requests.auth import HTTPDigestAuth
from http.server import HTTPServer, BaseHTTPRequestHandler
import telegram

telegram_bot = telegram.Bot(token=config('TELEGRAM_TOKEN'))
snapshot_request = Request('GET', config('SNAPSHOT_URL'), auth=HTTPDigestAuth(config('SNAPSHOT_AUTH_LOGIN'), config('SNAPSHOT_AUTH_PASSWORD')))
storage = Storage(config('STORAGE_DIR'))
watchdog = Watchdog(storage=storage, snapshot_request=snapshot_request, telegram_bot=telegram_bot, telegram_chat_id=config('TELEGRAM_CHAT_ID'))

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', '0')
        self.end_headers()

        if self.path == '/webhook':
            watchdog.pull_snapshot()
        elif self.path == '/send_image':
            watchdog.pull_snapshot()
            watchdog.send_snapshot()

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


httpd = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()

