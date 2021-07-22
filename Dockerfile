FROM python:3.7

WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y python3-opencv && pip install --no-cache-dir -r requirements.txt
COPY app /app

ENV STORAGE_DIR storage/

ENV CAMERA_IP 0.0.0.0
ENV CAMERA_PORT 80
ENV CAMERA_USERNAME ""
ENV CAMERA_PASSWORD ""

ENV TELEGRAM_TOKEN ""
ENV TELEGRAM_CHAT_ID ""
ENV NOMEROFF_API_URI ""

VOLUME ["/app/storage"]
EXPOSE 8000

ENTRYPOINT ["/app/http_server.py"]
HEALTHCHECK CMD curl -I --fail http://localhost:8000 || exit 1
