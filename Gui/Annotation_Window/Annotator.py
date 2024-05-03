import os
import cv2
from PySide6.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout
from PySide6.QtCore import QThread, Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, QColor, QPainter

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
        self.activeClass = None
        self.image = None
        self.lastImage = self.image

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self, a):
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def changeImage(self):
        if self.image.name != self.lastImage:
            p = QImage(self.image.name).scaled(640, 640)
            self.setImage(p)
            self.lastImage = self.image.name
