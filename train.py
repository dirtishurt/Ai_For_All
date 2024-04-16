import copy

import torch
from ultralytics import YOLO
import os



def runTrain(yaml_location):
    if torch.cuda.is_available():
        model = YOLO('yolov8n-seg.pt')
        results = model.train(data=os.path.abspath(yaml_location),
                              device=0, patience=20, cls=0.7, epochs=100)
    else:
        results = ("Failed to train, either run with CPU or check to see if you are using CONDA3.10 with PyTorch "
                   "installed")

    return results



