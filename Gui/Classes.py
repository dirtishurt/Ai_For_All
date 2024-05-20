import os

from PySide6.QtWidgets import (QWidget, QLabel, QApplication, QListWidget, QWidgetAction, QFileDialog, QVBoxLayout,
                               QPushButton, QGroupBox, QListWidgetItem, QHBoxLayout)
from PySide6.QtCore import QThread, Qt, Signal, Slot, QObject
from PySide6.QtGui import QImage, QPixmap, QColor


class Classes(QListWidget):
    def __init__(self, window):
        super().__init__(window)
        self.label = QLabel(window)
        self.classes = []
        self.title = 'Class Selector'

        # self.layout = QVBoxLayout()
        # self.frame = QGroupBox()
        self.setSpacing(1)
        self.setAcceptDrops(False)
        self.setSortingEnabled(False)
        self.initUI()
        self.last_key = None

        # self.th = Thread(self)

    def add_classes(self):
        self.clear()
        for i in range(len(self.classes)):
            if self.classes[i] == '':
                self.classes.__delitem__(i)
                i = 0
            if self.classes[i] == ' ':
                self.classes.__delitem__(i)
                i = 0
        for i in range(len(self.classes)):
            self.addItem(ClassButton((self.classes[i]), listview=self))


    def keyPressEvent(self, event):
        self.last_key = event.key()

    def initUI(self):
        self.add_classes()
        # self.setLayout(self.layout)

    def see_clicked(self):
        print(self.currentItem().name)

    def save_classes(self, working_directory):
        path = os.path.join(working_directory, 'classes.txt')
        file = open(path, 'w')
        for i in self.classes:
            file.write(i)
            file.write('\n')
        file.close()

    def load_classes(self, working_directory):
        path = os.path.join(working_directory, 'classes.txt')
        if os.path.exists(path):
            file = open(path, 'r')
            c = []
            for line in file:
                if line != '':
                    c.append(line.removesuffix('\n'))

            self.classes = c
            self.add_classes()


class ClassButton(QListWidgetItem):

    def __init__(self, name: str, listview):
        super().__init__(name, listview)
        self.name = name


