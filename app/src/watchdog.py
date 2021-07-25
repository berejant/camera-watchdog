from .storage import Storage
from .camera_client import CameraClient
from .image_recognizer import ImageRecognizer
import telegram
from src.number_detector import detect
from decouple import config
import re
import time
from typing import Optional

class Watchdog:
    storage: Storage
    camera_client: CameraClient
    telegram_bot: telegram.Bot
    telegram_chat_id: str
    current_snapshot: bytes
    current_state: dict
    car_number_pattern: re.Pattern

    def __init__(self, storage: Storage, camera_client: CameraClient, telegram_bot: telegram.Bot, telegram_chat_id: str):
        self.recognizer = ImageRecognizer()
        self.storage = storage
        self.camera_client = camera_client
        self.telegram_bot = telegram_bot
        self.telegram_chat_id = telegram_chat_id
        self.car_number_pattern = re.compile("^[A-Z]{2}[0-9]{4}[A-Z]{2}$")
        self.current_state = self.storage.load_state()
        self.pull_snapshot()

    def pull_snapshot(self):
        snapshot = self.camera_client.get_snapshot()
        if snapshot is None:
            return
        self.current_snapshot = snapshot
        self.storage.save_image(self.current_snapshot)

        previous_state = self.current_state
        self.current_state = self.recognizer.recognize(self.current_snapshot)
        self.storage.save_state(self.current_state)

        if previous_state is not None:
            self.execute_handlers(previous_state, self.current_state)

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

    def handle_is_not_parking_slot_free(self):
        text = "Паркинг занят"

        car_number = self.detect_car_number()
        if car_number is not None:
            text += " " + self.get_car_number_label(car_number)

        self.send_snapshot(text=text)

    def handle_is_gate_closed(self):
        print('gate closed')

    def handle_is_not_gate_closed(self):
        print('gate opened')

    def send_snapshot(self, text=None, disable_notification=False):
        self.telegram_bot.send_photo(
            chat_id=self.telegram_chat_id, disable_notification=disable_notification,
            photo=self.current_snapshot, caption=text
        )

    def detect_car_number(self) -> Optional[str]:
        retry_count = config("NOMEROFF_RETRY_COUNT", 3, cast=int)
        retry_delay = config("NOMEROFF_RETRY_DELAY", 3, cast=int)

        for attempt in range(retry_count):
            next_attempt_start_time = time.time() + retry_delay
            high_resolution = self.camera_client.get_high_resolution_snapshot()
            high_resolution = self.recognizer.crop_image_part_in_percent(high_resolution, 32, 96, 15, 73)
            car_number = detect(high_resolution)

            if car_number and self.car_number_pattern.match(car_number):
                return car_number

            next_attempt_delay = next_attempt_start_time - time.time()
            if next_attempt_delay > 0.2:
                time.sleep(next_attempt_delay)

        return None

    @staticmethod
    def get_car_number_label(car_number):
        return config('CAR_NUMBER_' + car_number[2:6], car_number)
