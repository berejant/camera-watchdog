from os import environ

print(environ)
config = {
    "STORAGE_DIR": "storage/",
    "SNAPSHOT_URL": None,
    "SNAPSHOT_AUTH_LOGIN": None,
    "SNAPSHOT_AUTH_PASSWORD": None,
    "TELEGRAM_TOKEN": None,
    "TELEGRAM_CHAT_ID": None,
}

for key in config:
    if key in environ:
        config[key] = environ[key]

print(config)
