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
            results = model(frame)

            an_frame = results[0].plot()

            cv2.imshow('Test', an_frame)
            cv2.waitKey(1)

