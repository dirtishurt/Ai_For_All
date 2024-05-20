import os
import cv2
from PySide6.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QComboBox
from PySide6.QtCore import QThread, Qt, Signal, Slot, QSize
from PySide6.QtGui import QImage, QPixmap
import torch
from ultralytics import YOLO
import time
pyqtSignal = Signal
pyqtSlot = Slot


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    getSize = pyqtSlot()

    def __init__(self, dataset, parent, conf):
        super().__init__()
        self.dataset = dataset
        self.parent = parent
        self.isRunning = True
        self.conf = conf
        time.sleep(.2)

    def run(self):
        exists = False
        if not torch.cuda.is_available():
            print("No CUDA capable GPU available, performance may be poor.")

        model = YOLO(os.path.abspath(self.dataset))
        cap = cv2.VideoCapture(0)
        while self.isRunning:

            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(self.render(model, frame), cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w,
                                           h, bytesPerLine,
                                           QImage.Format_RGB888).scaled(self.parent.size(),
                                                                        Qt.AspectRatioMode.KeepAspectRatio)
                self.changePixmap.emit(convertToQtFormat)
                cv2.waitKey(1)
        self.exit()


    def render(self, model, frame):
        results = model.predict(frame, conf=float(self.conf.value()/100), verbose=False)
        an_frame = results[0].plot()
        return an_frame


class Camera(QWidget):

    def __init__(self, a):
        super().__init__(a)
        self.a = a
        self.models = []
        self.model_selector = QComboBox()
        self.model = None
        self.oldLabel = QLabel(a)
        self.label = QLabel(a)
        self.th = None
        self.title = 'Camera'
        self.layout = QVBoxLayout()
        time.sleep(.2)

    @pyqtSlot(QImage)
    def setImage(self, image):
        # update image
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


    def initUI(self, a, v):
        self.th = Thread(a, self, v)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

