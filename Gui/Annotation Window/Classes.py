from PySide6.QtWidgets import (QWidget, QLabel, QApplication, QListWidget, QWidgetAction, QFileDialog, QVBoxLayout,
                               QPushButton, QGroupBox, QListWidgetItem)
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

        #self.th = Thread(self)

    def add_classes(self):
        self.clear()
        for i in range(len(self.classes)):
            self.addItem(ClassButton((self.classes[i]), listview=self))

    def initUI(self):
        self.add_classes()
        # self.setLayout(self.layout)

    def see_clicked(self):
        print(self.currentItem().name)


class ClassButton(QListWidgetItem):

    def __init__(self, name: str, listview):
        super().__init__(name, listview)
        self.name = name




