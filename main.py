import torch
from ultralytics import YOLO

torch.compile()

# as of right now the dataset will not work directily from the project directory, it needs to be in the default
# for ultralytics
print(torch.cuda.is_available())
if torch.cuda.is_available():
    if __name__ == '__main__':
        model = YOLO('yolov8n.pt')
        results = model.train(data='IDREC-2.v1i.yolov8/data.yaml', imgsz=640, epochs=1000, device=0)


