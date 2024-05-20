import os
import cv2
import google_images_search.cli
import google_images_search
from PySide6.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QGridLayout, QListWidgetItem
from PySide6.QtCore import QThread, Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, QColor, QPainter
from images_widget import Ui_Form

pyqtSignal = Signal
pyqtSlot = Slot


class Image_Search(QWidget):
    def __init__(self, parent=None, ann=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.display = self.ui.Preview
        self.files = self.ui.Images
        self.search = self.ui.Search

        self.number = self.ui.AMount
        self.last_key = None
        self.th = None
        self.image = None
        self.workingDirectory = None
        self.lastImage = None
        self.th = Search(self)
        self.files.itemClicked.connect(self.display.changeImage)


    def closeEvent(self, event) -> None:
        self.parent().show()

    def keyPressEvent(self, event) -> None:
        self.last_key = event.key()
        if self.last_key == Qt.Key.Key_Return:
            self.th.run()

    def showmethod(self):
        pth = os.path.join(self.workingDirectory, 'Searched_Images')
        if os.path.exists(pth):
            pass
        else:
            os.mkdir(pth)
        self.addexisting()

    def addexisting(self):
        pth = os.path.join(self.workingDirectory, 'Searched_Images')
        for i in os.listdir(pth):
            self.files.addItem(FileItem(os.path.join(pth, i), self.files, i))


class Search(QThread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def run(self):
        if self.parent.workingDirectory:
            if self.parent.last_key == Qt.Key.Key_Return:
                if self.parent.search.editingFinished:
                    if self.parent.number.editingFinished:
                        gis = google_images_search.GoogleImagesSearch('AIzaSyAjKQXeIqyDFtauG71OoffKTYfluuGnQ8U',
                                                                      '06526dcf3143f4769')
                        self.parent.last_key = None
                        _search_params = {
                            'q': self.parent.search.text(),
                            'num': int(self.parent.number.text()),
                            'fileType': 'jpg|png',
                            'rights': 'cc_noncommercial',
                            'safe': 'safeUndefined',
                            'imgType': 'imgTypeUndefined',
                            'imgSize': 'imgSizeUndefined',
                            'imgDominantColor': 'imgDominantColorUndefined',
                            ##
                            'imgColorType': 'color'
                        }
                        pth = os.path.join(self.parent.workingDirectory, 'Searched_Images')
                        if os.path.exists(pth):
                            pass
                        else:
                            os.mkdir(pth)
                        gis.search(search_params=_search_params, path_to_dir=pth, width=640,
                                   height=640)

                        for i in os.listdir(pth):
                            self.parent.files.clear()
                            self.parent.files.addItem(FileItem(os.path.join(pth, i), self.parent.files, i))


class FileItem(QListWidgetItem):

    def __init__(self, name: str, listview, baseName: str):
        super().__init__(name, listview)
        self.name = name
        self.base = baseName
        self.setText(self.base)
