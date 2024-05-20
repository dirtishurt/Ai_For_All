import os

from PySide6.QtWidgets import (QWidget, QLabel, QApplication, QListWidget, QWidgetAction, QFileDialog, QVBoxLayout,
                               QListWidgetItem, QScrollBar)
from PySide6.QtCore import QThread, Qt, Signal, Slot, QStringListModel
from PySide6.QtGui import QImage, QPixmap, QColor, QDropEvent


class Files(QListWidget):
    file_selected = Signal()
    def __init__(self, window):
        super().__init__(window)

        self.label = QLabel(window)
        self.th = None
        self.title = 'Files'
        self.layout = QVBoxLayout()
        self.dialog = QFileDialog(self, caption='Select Image Directory')
        self.dialog.setFileMode(QFileDialog.FileMode.Directory)
        self.setVerticalScrollBar(QScrollBar())
        self.open = True
        self.dialog.setViewMode(QFileDialog.ViewMode.Detail)
        self.last = None
        self.filenames = ''
        self.setSortingEnabled(False)
        self.setSpacing(1)
        self.ref = None

    def getFiles(self, a=1, working_dir=None):
        if a == 1:
            if self.currentItem() is not None:
                self.currentItem().setSelected(False)
                self.ref = None
                self.filenames = ''
            self.clear()
            if self.dialog.exec():
                self.filenames = self.dialog.selectedFiles()
                self.printfilenames()
                self.save_image_paths(working_dir)
                self.setCurrentItem(self.item(0))
        if a == 2:
            if self.dialog.exec():
                self.filenames = self.dialog.selectedFiles()
                self.printfilenames()
                self.save_image_paths(working_dir, 'a')
                self.setCurrentItem(self.item(0))

    def save_image_paths(self, working_directory, mode='w'):
        path = os.path.join(working_directory, 'image_paths.txt')
        file = open(path, mode)
        file.write(f'{self.filenames[0]}\n')
        file.close()

    @Slot()
    def update_last(self):
        self.last = self.currentItem()

    @staticmethod
    def clearImagePaths(working_directory):
        path = os.path.join(working_directory[0], 'image_paths.txt')
        file = open(path, 'w')
        file.write('')
        file.close()

    def printfilenames(self):
        for i in os.listdir(self.filenames[0]):
            path = os.path.join(self.filenames[0], i)
            if os.path.isdir(path):
                self.recursive_add(path)
            else:
                newitem = FileItem(path, self, i)
                self.addItem(newitem)

    def recursive_add(self, path):
        if os.path.isdir(path):
            for i in os.listdir(path):
                f_path = os.path.join(path, i)
                if os.path.isdir(f_path):
                    self.recursive_add(f_path)
                else:
                    newitem = FileItem(f_path, self, i)
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

    def current(self):
        self.see_clicked(0)


class FileItem(QListWidgetItem):

    def __init__(self, name: str, listview, baseName: str):
        super().__init__(name, listview)
        self.name = name
        self.base = baseName
        self.setText(self.base)
