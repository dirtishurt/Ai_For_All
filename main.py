import cv2
from ultralytics import YOLO
import cvzone

model = YOLO('yolov8n.pt')

results = model.train(data='coco8.yaml', epochs=100, imgsz=640)