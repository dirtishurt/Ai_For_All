import cv2
from ultralytics import YOLO
import os

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.open(0)


def render(dataset):
    model = YOLO(os.path.abspath(dataset))

    while capture.isOpened():
        ret, frame = capture.read()
        if ret:
            results = model.predict(frame, conf=.56, verbose=True)

            print(results[0].boxes.cls, results[0].boxes.conf)

            an_frame = results[0].plot()

            return an_frame



