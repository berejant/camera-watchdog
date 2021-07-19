from requests import Session, Request
from .storage import Storage
from .image_recognizer import ImageRecognizer


class Watchdog:
    storage: Storage
    session: Session
    snapshot_request: Request
    current_state: dict

    def __init__(self, storage: Storage, snapshot_request: Request):
        self.session = Session()
        self.recognizer = ImageRecognizer()
        self.storage = storage
        self.snapshot_request = snapshot_request
        self.current_state = self.storage.load_state()

    def pull_snapshot(self):
        response = self.session.send(self.snapshot_request.prepare())
        self.storage.save_image(response.content)

        previous_state = self.current_state
        self.current_state = self.recognizer.recognize(response.content)
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
        print('parking slot free')

    def handle_is_not_parking_slot_free(self):
        print('parking slot free')

    def handle_is_gate_closed(self):
        print('gate closed')

    def handle_is_not_gate_closed(self):
        print('gate opened')
