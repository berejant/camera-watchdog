import schedule
import time
from pathlib import Path
from datetime import datetime, timedelta
import os
import shutil
import json
from typing import Optional


class Storage:
    base_dir: str
    state_filename = 'state.json'

    def __init__(self, base_dir):
        self.base_dir = base_dir + '/'
        schedule.every().day.at("00:01").do(self.clear_outdated_files)
        self.clear_outdated_files()

    def save_image(self, image: bytes):
        dir = self.base_dir + time.strftime("%Y-%m-%d")
        Path(dir).mkdir(parents=True, exist_ok=True)
        filename = time.strftime("%Y-%m-%d-%H-%M-%S") + '.jpg'
        with open(dir + '/' + filename, "wb") as f:
            f.write(image)

    def clear_outdated_files(self):
        min_datetime = datetime.now() - timedelta(days=3)
        for dir in os.listdir(self.base_dir):
            if not os.path.isdir(self.base_dir + dir):
                continue
            try:
                dir_date = datetime.strptime(dir, "%Y-%m-%d")
                delete_dir = dir_date < min_datetime
            except ValueError:
                delete_dir = True
            if delete_dir:
                shutil.rmtree(self.base_dir + dir)

    def load_state(self) -> Optional[dict]:
        try:
            with open(self.base_dir + self.state_filename, "r") as f:
                return json.loads(f.read())
        except (ValueError, FileNotFoundError):
            return None

    def save_state(self, state: dict):
        with open(self.base_dir + self.state_filename, "w") as f:
            f.write(json.dumps(state))
