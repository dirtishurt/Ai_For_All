# This Python file uses the following encoding: utf-8
import os
import sys
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidgetAction, QFileDialog
import PySide6.QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
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
        self.active = None

    @Slot(bool)
    def getFiles(self):
        if self.imgsAdd.actionAt(QWidgetAction.triggered):
            self.imgsAdd.emit(str(QFileDialog.getExistingDirectory(self, 'Select Directory')))

    def getactions(self):
        # threadCount = QThreadPool.globalInstance().maxThreadCount()
        pool = QThreadPool.globalInstance()

        self.runner = Runnable(self.toolbar.actions())
        pool.start(self.runner)

    @Slot(QAction)
    def getActive(self, i):
        if i.isChecked():
            print(i.text())
            if self.active != i:
                if self.active is not None:
                    self.active.toggle()
                self.active = i
                if self.active.text() == 'delete':
                    self.active.toggle()
                    self.active = None



class Runnable(QRunnable, QObject):
    getWidgets = Signal(QAction)

    def __init__(self, n):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.n = n
        self.running = True

    def run(self):
        while self.running:
            for i in self.n:
                if i.text() != '':
                    self.getWidgets.emit(i)
                    time.sleep(.05)

    def stop(self):
        self.running = False


if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = MainWindow()

    widget.show()
    widget.getactions()
    # ALL Signals below this comment

    widget.runner.getWidgets.connect(widget.getActive)
    if app.exit():
        widget.runner.stop()
    sys.exit(app.exec())
