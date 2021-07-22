from requests import Session, Request
from requests.exceptions import RequestException
from .storage import Storage
from .image_recognizer import ImageRecognizer
from urllib.parse import urlparse
import cv2
import numpy as np
import telegram

class Watchdog:
    storage: Storage
    session: Session
    snapshot_request: Request
    telegram_bot: telegram.Bot
    telegram_chat_id: str
    current_snapshot: bytes
    current_state: dict

    def __init__(self, storage: Storage, snapshot_request: Request, telegram_bot: telegram.Bot, telegram_chat_id: str):
        self.session = Session()
        self.recognizer = ImageRecognizer()
        self.storage = storage
        self.snapshot_request = snapshot_request
        self.telegram_bot = telegram_bot
        self.telegram_chat_id = telegram_chat_id
        self.current_state = self.storage.load_state()
        self.pull_snapshot()

    def pull_snapshot(self):
        try:
            response = self.session.send(self.snapshot_request.prepare(), timeout=1)
            self.current_snapshot = response.content
            self.storage.save_image(self.current_snapshot)

            previous_state = self.current_state
            self.current_state = self.recognizer.recognize(self.current_snapshot)
            self.storage.save_state(self.current_state)

            if previous_state is not None:
                self.execute_handlers(previous_state, self.current_state)
        except RequestException:
            print('Failed to get snapshot')

    def get_high_resolution_snapshot(self) -> np.ndarray:
        # @todo Implement onfiv support and getting Snapshot and MediaStream url from onvif
        url = urlparse(self.snapshot_request.url)
        auth = self.snapshot_request.auth
        host, port = url.netloc.split(':')
        cap = cv2.VideoCapture('rtsp://' + auth.username + ':' + auth.password + '@' + host + ':554/ch01/0')
        ret, frame = cap.read()

        if cap.isOpened():
            _, frame = cap.read()
            cap.release()  # releasing camera immediately after capturing picture
            if _ and frame is not None:
                return frame

    def execute_handlers(self, previous_state, new_state):
        key: str
        for key in new_state:
            if new_state[key] != previous_state[key]:
                method = key
                if not new_state[key] and key.startswith('is_'):
                    method = 'is_not_' + method[3:]
                method = 'handle_' + method

                getattr(self, method)()

    def handle_is_parking_slot_free(self):
        self.send_snapshot(text="Паркинг свободен")
        print('parking slot free')

    def handle_is_not_parking_slot_free(self):
        self.send_snapshot(text="Паркинг занят")
        print('parking slot free')

    def handle_is_gate_closed(self):
        print('gate closed')

    def handle_is_not_gate_closed(self):
        print('gate opened')

    def send_snapshot(self, text=None):
        self.telegram_bot.send_photo(chat_id=self.telegram_chat_id, photo=self.current_snapshot, caption=text)

