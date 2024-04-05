from ultralytics import YOLO
from roboflow import Roboflow
import subprocess
#rf = Roboflow(api_key="TMwL4aTXfDBeX60bnsFu")
#project = rf.workspace("idrec").project("idrec")
#dataset = project.version(1).download('YOLOv8n-cls.pt')

model = YOLO('yolov8n-cls.pt')
mode = 'train'


