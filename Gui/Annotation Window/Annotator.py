import os
import cv2
from PySide6.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout
from PySide6.QtCore import QThread, Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, QColor

pyqtSignal = Signal
pyqtSlot = Slot


class Annotator(QWidget):
    def __init__(self, a):
        super().__init__(a)
        self.label = QLabel(a)
        self.th = None
        self.title = 'Annotator'
        self.layout = QVBoxLayout()
        self.initUI(a)



    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self, a):
        self.th = Thread(self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.isRunning = True
        while self.isRunning:
            p = QImage('1595270639570.jpg').scaled(640, 640, Qt.KeepAspectRatioByExpanding)

            self.changePixmap.emit(p)

    def stop(self):
        self.isRunning = False
        self.quit()
        self.terminate()

