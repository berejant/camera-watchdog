#!/usr/bin/env python3
from decouple import config
from src.storage import Storage
from src.camera_client import CameraClient
from src.watchdog import Watchdog
from http.server import HTTPServer
from src.http_handler import WatchdogHTTPRequestHandler
import telegram

camera_client = CameraClient(config('CAMERA_IP'), config('CAMERA_PORT', 80),
                      config('CAMERA_USERNAME'), config('CAMERA_PASSWORD'))
telegram_bot = telegram.Bot(token=config('TELEGRAM_TOKEN'))
storage = Storage(config('STORAGE_DIR'))
watchdog = Watchdog(storage=storage, camera_client=camera_client, telegram_bot=telegram_bot, telegram_chat_id=config('TELEGRAM_CHAT_ID'))

http_handler = WatchdogHTTPRequestHandler(watchdog=watchdog)
httpd = HTTPServer(('0.0.0.0', 8000), http_handler)
httpd.serve_forever()
