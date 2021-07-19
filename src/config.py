from os import path, environ as env
from shutil import copyfile
from dotenv import load_dotenv

path.exists('.env') or copyfile('.env.example', '.env')
load_dotenv()

config = {
    "STORAGE_DIR": "storage/",
    "SNAPSHOT_URL": None,
    "SNAPSHOT_AUTH_LOGIN": None,
    "SNAPSHOT_AUTH_PASSWORD": None,
}

for key in config:
    if key in env:
        config[key] = env[key]
