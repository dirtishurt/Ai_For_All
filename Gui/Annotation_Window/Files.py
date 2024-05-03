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
        self.setSortingEnabled(False)
        self.setSpacing(1)
        self.ref = None

    def getFiles(self, a=1):
        if a == 1:
            if self.currentItem() is not None:
                self.currentItem().setSelected(False)
                self.ref = None
                self.filenames = ''
            self.clear()
            if self.dialog.exec():
                self.filenames = self.dialog.selectedFiles()
                self.printfilenames()
                self.setCurrentItem(self.item(0))
        if a == 2:
            if self.dialog.exec():
                self.filenames = self.dialog.selectedFiles()
                self.printfilenames()
                self.setCurrentItem(self.item(0))

    def printfilenames(self):
        for i in os.listdir(self.filenames[0]):
            path = os.path.join(self.filenames[0], i)

            newitem = FileItem(path, self, i)
            self.addItem(newitem)

    def see_clicked(self, f):
        if self.ref is not None:
            nxt = (self.indexFromItem(self.ref).row()) + f
            self.setCurrentItem(self.item(nxt))
            print(self.ref)

    def next(self):
        self.see_clicked(1)

    def prev(self):
        self.see_clicked(-1)


class FileItem(QListWidgetItem):

    def __init__(self, name: str, listview, baseName: str):
        super().__init__(name, listview)
        self.name = name
        self.base = baseName
