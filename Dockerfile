FROM tensorflow/tensorflow:2.3.2

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y git libsm6 libxrender1 libgl1 libfontconfig1 libxtst6 libturbojpeg

WORKDIR /app
COPY app/src/number_detector.py /app/src/number_detector.py
RUN git clone  https://github.com/ria-com/nomeroff-net.git \
  && cd nomeroff-net/ \
  && sed -i 's/^tensorflow/#&/' requirements.txt \
  && pip install --no-cache-dir -r requirements.txt \
  && cd ../ \
  && python src/number_detector.py

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app /app

ENV STORAGE_DIR storage/

ENV CAMERA_IP 0.0.0.0
ENV CAMERA_PORT 80
ENV CAMERA_USERNAME ""
ENV CAMERA_PASSOWRD ""

ENV TELEGRAM_TOKEN ""
ENV TELEGRAM_CHAT_ID ""

VOLUME ["/app/storage", "/app/nomeroff-net/NomeroffNet/Base/mcm/data/models"]
EXPOSE 8000

ENTRYPOINT ["/app/http_server.py"]
HEALTHCHECK CMD curl -I --fail http://localhost:8000 || exit 1
