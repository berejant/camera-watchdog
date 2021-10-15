FROM python:3.7

WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends python3-opencv=4.5.1+dfsg-5 && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY app /app

ENV STORAGE_DIR storage/

ENV CAMERA_IP 0.0.0.0
ENV CAMERA_PORT 80
ENV CAMERA_USERNAME ""
ENV CAMERA_PASSWORD ""

ENV TELEGRAM_TOKEN ""
ENV TELEGRAM_CHAT_ID ""

ENV NOMEROFF_API_URI ""
ENV NOMEROFF_RETRY_DELAY 5
ENV NOMEROFF_RETRY_COUNT 6

VOLUME ["/app/storage"]
EXPOSE 8000

ENTRYPOINT ["/app/http_server.py"]
HEALTHCHECK CMD curl -I --fail http://localhost:8000 || exit 1
