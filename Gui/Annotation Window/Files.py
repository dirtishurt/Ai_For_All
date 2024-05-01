import os

from PySide6.QtWidgets import (QWidget, QLabel, QApplication, QListWidget, QWidgetAction, QFileDialog, QVBoxLayout,
                               QListWidgetItem, QScrollBar)
from PySide6.QtCore import QThread, Qt, Signal, Slot, QStringListModel
from PySide6.QtGui import QImage, QPixmap, QColor, QDropEvent


class Files(QListWidget):
    def __init__(self, window):
        super().__init__(window)

        self.label = QLabel(window)
        self.th = None
        self.title = 'Files'
        self.layout = QVBoxLayout()
        self.dialog = QFileDialog(self)
        self.dialog.setFileMode(QFileDialog.FileMode.Directory)
        self.setVerticalScrollBar(QScrollBar())

        self.dialog.setViewMode(QFileDialog.ViewMode.Detail)
        self.filenames = ''
        self.setSortingEnabled(True)
        self.setSpacing(1)

        self.initUI()

    def initUI(self):
        if self.dialog.exec():
            self.filenames = self.dialog.selectedFiles()
        self.printfilenames()

    def printfilenames(self):
        for i in os.listdir(self.filenames[0]):
            path = os.path.join(self.filenames[0], i)
            newitem = FileItem(path, self)
            self.addItem(newitem)

    def see_clicked(self):
        for index in self.selectedIndexes():
            print(index)

class FileItem(QListWidgetItem):

    def __init__(self, name: str, listview):
        super().__init__(name, listview)
        self.name = name
