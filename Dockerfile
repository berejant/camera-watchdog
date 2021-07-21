FROM tensorflow/tensorflow:2.3.2

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y git libsm6 libxrender1 libgl1 libfontconfig1 libxtst6 libturbojpeg

WORKDIR /app
RUN git clone  https://github.com/ria-com/nomeroff-net.git \
  && cd nomeroff-net/ \
  && sed -i 's/^tensorflow/#&/' requirements.txt \
  && pip install --no-cache-dir -r requirements.txt \
  && cd ../

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app /app
ENV STORAGE_DIR storage/

VOLUME ["/app/storage", "/app/nomeroff-net/NomeroffNet/Base/mcm/models"]
EXPOSE 8000

ENTRYPOINT ["/app/webhook_listener.py"]
HEALTHCHECK CMD curl -I --fail http://localhost:8000 || exit 1