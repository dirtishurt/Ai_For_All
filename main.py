
from ultralytics import YOLO
import os

if __name__ == "__main__":
    model = YOLO("yolov8n-cls.pt")
    model.info()
    results = model.train(data="detect",epochs=100,imgsz=640)
