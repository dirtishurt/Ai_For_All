from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextBrowser, QWidget, QMenu
from PySide6.QtCore import Signal, Slot, QRunnable, QObject, Qt, QThreadPool, QUrl, QEvent
from PySide6.QtGui import QAction, Qt


class Github(QMenu):
    def __init__(self, window):
        super().__init__(window)
        self.key = None

    def mousePressEvent(self, arg__1):
        self.key = arg__1.button()


    def get_mouse_event(self):
        if self.key == Qt.MouseButton.LeftButton:
            self.key = None
            return True
        return False
