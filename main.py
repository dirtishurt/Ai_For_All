import os.path

# DO NOT MOVE THIS NEXT LINE OF CODE, IT HAS TO RUN WITH THE IMPORT STATMENTS, THE CODE WILL NOT WORK
import torch
import combineTrain
import combine_data
from ultralytics import YOLO

torch.compile()
# as of right now the dataset will not work directily from the project directory, it needs to be in the default
# for ultralytics
# --fixed

# tr = input('Train Model Y/n')


if __name__ == '__main__':
    # combineTrian.addData('./Working_Models/yolov8segment/best.pt',
    #                   './Datasets/yolov8seg/IDREC-3-ONESHOTS 2.v2i.yolov8/data.yaml')
    # combineTrian.newModel()
    #combineTrain.combineTrain('CombinedDatasets/2024-04-15 07039', 'Working_Models/yolov8segment/best.pt')
    # combineTrain.createTrainingSet('Working_Models/yolov8segment/best.pt', 'Datasets/yolov8seg/IDREC-3-ONESHOTS 2.v2i.yolov8')
    #print(len(dict(YOLO('Working_Models/yolov8segment/best.pt').named_modules())))
    model = YOLO('yolov8n-seg.pt')
    model.train(epochs=40, warmup_epochs=0, pretrained='./Working_Models/yolov8segment/best.pt', freeze=22,
                data=os.path.abspath('Cool/11470343422024-04-17/data.yaml'))
