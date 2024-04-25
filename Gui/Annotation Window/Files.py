from PySide6.QtWidgets import QWidget, QLabel, QApplication, QListWidget, QWidgetAction, QFileDialog
from PySide6.QtCore import QThread, Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, QColor

class Files(QListWidget):
    def __init__(self, window):
        super().__init__(window)




