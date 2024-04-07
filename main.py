import torch
from ultralytics import YOLO
import os

torch.compile()


# as of right now the dataset will not work directily from the project directory, it needs to be in the default
# for ultralytics
# --fixed

# tr = input('Train Model Y/n')
def runTrain():
    if torch.cuda.is_available():
        model = YOLO('yolov8s-seg.pt')
        results = model.train(data=os.path.abspath('./Datasets/yolov8/IDREC-3.v1i.yolov8/data.yaml'),
                              device=0, patience=30, cls=0.7)

    else:
        model = YOLO('yolov8s-seg.pt')
        if input("Non-CUDA compatible GPU detected... proceed with CPU? y/n").lower() == 'y':
            results = model.train(data=os.path.abspath('./Datasets/yolov8/IDREC-3.v1i.yolov8/data.yaml'),
                                  patience=30, plots=True, cls=.7)
        else:
            results = ("Failed to train, either run with CPU or check to see if you are using CONDA3.10 with PyTorch "
                       "installed")

    return results


if __name__ == '__main__':
    rs = runTrain()
