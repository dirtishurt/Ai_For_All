import os
import sys
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ultralytics import YOLO

import camera
import cv2


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        page_layout = QHBoxLayout()
        info_layout = QVBoxLayout()

        self.FeedLabel = QLabel()
        page_layout.addWidget(self.FeedLabel)

        self.LineEdit = QLineEdit()
        self.LineEdit.setPlaceholderText("Enter New Name")
        page_layout.addWidget(self.LineEdit)

        self.EnterBTN = QPushButton("Enter")
        self.EnterBTN.setCheckable(True)
        self.EnterBTN.clicked.connect(self.EnterInfo)
        page_layout.addWidget(self.EnterBTN)
        a = run('./Working_Models/yolov8segment/best.pt')
        pixmap = QPixmap(a)
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        page_layout.addWidget(lbl)

        info_layout.addWidget(self.LineEdit)
        info_layout.addWidget(self.EnterBTN)
        info_layout.addLayout(page_layout)
        self.setLayout(info_layout)

    def EnterInfo(self):
        new_info = self.get_name()
        print(new_info)

    def get_name(self):
        person_name = self.LineEdit.text()
        return person_name


def run(dataset):
    ThreadActive = True
    model = YOLO(os.path.abspath(dataset))
    Capture = cv2.VideoCapture(0)
    while ThreadActive:
        ret, frame = Capture.read()
        if ret:
            results = model.predict(frame, conf=.56, verbose=True)
            # Optional
            # print(results[0].boxes.cls, results[0].boxes.conf)

            an_frame = results[0].plot()

            cv2.waitKey(1)
            if an_frame is not None:
                return an_frame


class MyWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QGridLayout()
        self.setLayout(self.layout)


App = QApplication(sys.argv)
Root = MainWindow()

Root.show()

sys.exit(App.exec())
