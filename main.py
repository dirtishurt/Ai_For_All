import torch
from ultralytics import YOLO
import os

torch.compile()

# as of right now the dataset will not work directily from the project directory, it needs to be in the default
# for ultralytics
#--fixed

#tr = input('Train Model Y/n')

if torch.cuda.is_available():
    if __name__ == '__main__':
        model = YOLO('yolov8n.pt')
        results = model.train(data=os.path.abspath('./Datasets/IDREC-2.v6i.yolov8/data.yaml'), imgsz=640, epochs=1000, device=0)

#else:
    #


