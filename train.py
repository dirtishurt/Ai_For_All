import copy

import torch
from ultralytics import YOLO
import os


#TODO Implement this in the gui
def runTrain(yaml_location):
    if torch.cuda.is_available():
        model = YOLO('yolov8n-seg.pt')
        results = model.train(data=os.path.abspath(yaml_location),
                              device=0, patience=10, cls=2, epochs=100, pretrained='Working_Models/yolov8segment/best.pt')
    else:
        results = ("Failed to train, either run with CPU or check to see if you are using CONDA3.10 with PyTorch "
                   "installed")

    return results



if __name__ == '__main__':
    runTrain('S/data.yaml')
