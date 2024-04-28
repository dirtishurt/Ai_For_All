from PySide6.QtWidgets import QWidget, QLabel, QApplication, QListWidget, QWidgetAction, QFileDialog, QVBoxLayout
from PySide6.QtCore import QThread, Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, QColor


class Files(QListWidget):
    def __init__(self, window):
        super().__init__(window)
        self.label = QLabel(window)
        self.th = None
        self.title = 'Files'
        self.layout = QVBoxLayout()
        self.setAcceptDrops(True)
        self.setSortingEnabled(True)
