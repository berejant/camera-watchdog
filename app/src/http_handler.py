from http.server import BaseHTTPRequestHandler
from src.watchdog import Watchdog


class WatchdogHTTPRequestHandler(BaseHTTPRequestHandler):
    watchdog: Watchdog

    def __init__(self, watchdog: Watchdog, *args, **kwargs) -> None:
        self.watchdog = watchdog
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', '0')
        self.end_headers()

        if self.path == '/webhook':
            self.watchdog.pull_snapshot()
        elif self.path == '/send_image':
            self.watchdog.pull_snapshot()
            self.watchdog.send_snapshot()

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
