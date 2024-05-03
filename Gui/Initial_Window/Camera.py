import os

import cv2
from PySide6.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout
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
        self.isRunning = True
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
        self.isRunning = False
        self.quit()
        self.terminate()

    def render(self, model, frame):
        results = model.predict(frame, conf=.56, verbose=False)
        an_frame = results[0].plot()
        return an_frame


class Camera(QWidget):
    def __init__(self, a):
        super().__init__(a)
        self.label = QLabel(a)
        self.th = None
        self.title = 'Camera'
        self.layout = QVBoxLayout()
        self.initUI(a)

    @pyqtSlot(QImage)
    def setImage(self, image):
        # update image
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self, a):
        self.th = Thread(self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()
