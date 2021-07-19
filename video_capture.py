#!/usr/bin/env python3
import cv2
from src.config import config
print(config)
cap = cv2.VideoCapture('rtsp://' + config['SNAPSHOT_AUTH_LOGIN']  + ':' + config['SNAPSHOT_AUTH_PASSWORD'] + '@192.168.88.167:554/ch01/0')

ret, frame = cap.read()

if cap.isOpened():
    _,frame = cap.read()
    cap.release() #releasing camera immediately after capturing picture
    if _ and frame is not None:
        cv2.imwrite('latest.jpg', frame)

