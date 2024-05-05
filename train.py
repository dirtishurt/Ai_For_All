import copy

import torch
from ultralytics import YOLO
import os

torch.compile()

torch.cuda.init()


# TODO Implement this in the gui and fix the labels being broken
def runTrain(yaml_location, epochs=100, patience=20, devices=None, pretrained=False,
             modelLocation='Working_Models/base-ultralytics/yolov8n-seg.pt'):
    """
    epochs adjusts length of training, patience adjusts the time it waits for improvement,
    do not add devices unless a cuda compatible gpu is detected


    """
    modelLocation = os.path.abspath(modelLocation)
    model = YOLO(modelLocation)
    results = model.train(data=os.path.abspath(yaml_location),
                          device=devices,
                          patience=patience, epochs=epochs, pretrained=pretrained)

    return results

if __name__ == '__main__':
    runTrain('An_Prj1/dataset_3608924368837/data.yaml')
