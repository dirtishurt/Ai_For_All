# This Python file uses the following encoding: utf-8
import os
import sys
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidgetAction, QFileDialog
import PySide6.QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QThread, QObject, QRunnable, QThreadPool, Signal, Slot
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.toolbar = self.ui.toolBar
        self.runner = None
        self.imgsAdd = self.ui.menuOpen_Images

    @Slot(bool)
    def getFiles(self):
        if self.imgsAdd.actionAt(QWidgetAction.triggered):
            self.imgsAdd.emit(str(QFileDialog.getExistingDirectory(self, 'Select Directory')))

    def getactions(self):
        # threadCount = QThreadPool.globalInstance().maxThreadCount()
        pool = QThreadPool.globalInstance()

        self.runner = Runnable(self.toolbar.actions())
        pool.start(self.runner)


class Tools:
    def __init__(self, tool_type):
        self.tool = tool_type

    def setTool(self):
        if self.tool == 'Poly':
            return 0
        if self.tool == 'Box':
            return 1
        if self.tool == 'Trash':
            return 2
        else:
            return -1


class Runnable(QRunnable):
    def __init__(self, n):
        super().__init__()
        self.n = n
        self.running = True
    getFiles = Signal(bool)
    def run(self):

        while self.running:
            for i in self.n:
                if i.text() != '':
                    # print(i.isChecked())
                    
                    time.sleep(.5)

    def stop(self):
        self.running = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    widget.getactions()
    if app.exit():
        widget.runner.stop()
    sys.exit(app.exec())
