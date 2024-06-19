from PySide6.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QGridLayout, QListWidgetItem
from PySide6.QtCore import QThread, Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, QColor, QPainter

class Display(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel(parent)
        self.label.setScaledContents(True)
        self.layout = QGridLayout()
        self.image = None
        self.lastImage = None
        self.parent = parent
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def changeImage(self):
        self.image = self.parent.files.currentItem()
        if self.image.name != self.lastImage:
            p = QImage(self.image.name)
            self.setImage(p)
            self.lastImage = self.image.name

    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImageInPlace(image))

