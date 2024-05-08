import copy

import torch
from ultralytics import YOLO
import os
import math

# TODO Implement this in the gui and fix the labels being broken
def runTrain(yaml_location, epochs=100, patience=20,
             modelLocation=None, export_path=None, progress=None):
    torch.compile()
    torch.cuda.init()

    """
    epochs adjusts length of training, patience adjusts the time it waits for improvement,
    do not add devices unless a cuda compatible gpu is detected


    """
    modelLocation = os.path.abspath(modelLocation)
    model = YOLO(modelLocation)
    if torch.cuda.is_available():
        print('CUDA Compatible Detected, Starting Training')
        model.train(data=yaml_location, device=0, patience=patience, epochs=epochs,
                    imgsz=640, project=export_path, verbose=True)
        for epoch in range(model.trainer.epochs - 1, model.trainer.epochs):
            progress.setValue(math.ceil(epoch / epochs))
    else:
        print('WARNING CUDA COMPATIBLE GPU NOT DETECTED, TRAINING WILL TAKE LONGER...')
        model.train(data=yaml_location, device='cpu', patience=patience,
                    epochs=epochs,
                    imgsz=640, project=export_path, verbose=False)
        for epoch in range(model.trainer.epochs - 1, model.trainer.epochs):
            progress.setValue(math.ceil(epoch / epochs))
