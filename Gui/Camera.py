import os

import cv2
from PySide6.QtWidgets import  QWidget, QLabel, QApplication
from PySide6.QtCore import QThread, Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
import torch
from ultralytics import YOLO

pyqtSignal = Signal
pyqtSlot = Slot
class Thread(QThread):


    changePixmap = pyqtSignal(QImage)
    def run(self):
        exists = False
        if not torch.cuda.is_available():
            print("No CUDA capable GPU available, performance may be poor.")
        while not exists:
            self.dataset = os.path.abspath(input('Enter Path').strip())
            exists = os.path.exists(self.dataset)
        self.isRunning=True
        model = YOLO(os.path.abspath(self.dataset))
        cap = cv2.VideoCapture(0)
        while self.isRunning:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(self.render(model, frame), cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(460, 390, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                cv2.waitKey(1)

    def stop(self):
        self.isRunning=False
        self.quit()
        self.terminate()

    def render(self, model, frame):
        results = model.predict(frame, conf=.56, verbose=False)
        an_frame = results[0].plot()
        return an_frame

class Camera(QWidget):
    def __init__(self, a):
        super().__init__()
        self.title = 'PySide Video'
        self.left = 20
        self.top = 20
        self.fwidth = 460
        self.fheight = 390
        self.initUI(a)
    @pyqtSlot(QImage)
    def setImage(self, image):
        #update image
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self, a):
        self.setGeometry(self.left, self.top, self.fwidth, self.fheight)
        self.resize(self.fwidth, self.fheight)

        # create a label
        self.label = QLabel(a)
        self.label.resize(self.fwidth, self.fheight)
        self.label.move(self.left, self.top)
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

