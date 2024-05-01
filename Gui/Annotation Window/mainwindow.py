# This Python file uses the following encoding: utf-8
import os
import sys
import time

from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidgetAction, QFileDialog
import PySide6.QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction, QKeyEvent, QColor, QPixmap
from PySide6.QtCore import QThread, QObject, QRunnable, QThreadPool, Signal, Slot, Qt, QEvent, QSize
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow


class MainWindow(QMainWindow):
    keysPressed = Signal(QEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_key = None
        self.file_path = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.toolbar = self.ui.toolBar
        self.runner = None
        self.runner2 = None
        self.imgsAdd = self.ui.menuOpen_Images
        self.active = None
        self.lastActive = None
        self.lineedit = self.ui.lineEdit
        self.classes = self.ui.Classes
        self.files = self.ui.Files
        self.annotator = self.ui.Annotator
        self.draw = self.ui.Draw

    @Slot(bool)
    def getFiles(self):
        if self.imgsAdd.actionAt(QWidgetAction.triggered):
            self.imgsAdd.emit(str(QFileDialog.getExistingDirectory(self, 'Select Directory')))

    def keyPressEvent(self, event):
        self.last_key = event.key()

    def send_line_output(self):
        if self.lineedit.editingFinished:
            if self.last_key == Qt.Key.Key_Return:
                if self.lineedit.text() not in self.classes.classes:
                    self.classes.classes.append(self.lineedit.text())
                    self.classes.add_classes()
                self.lineedit.clear()
                self.last_key = None

    def getactions(self):
        # threadCount = QThreadPool.globalInstance().maxThreadCount()
        pool = QThreadPool.globalInstance()

        self.runner = Runnable(self.toolbar.actions())
        self.runner2 = OtherLoop(self)
        pool.start(self.runner)
        pool.start(self.runner2)

    @Slot(QAction)
    def getActive(self, i):
        if i.isChecked():
            if self.active != i:
                if self.active is not None:
                    self.active.toggle()
                self.active = i
            if self.active.text() == 'delete':
                self.active.toggle()
                self.draw.clearCanvas()
            if self.active.text() == 'Undo':
                self.active.toggle()
                self.draw.undo()

    @Slot()
    def loop(self):
        self.send_line_output()
        if self.files.currentItem() is not None:
            self.annotator.image = self.files.currentItem().name
            self.annotator.changeImage()
            if self.classes.currentItem() is not None:
                self.annotator.activeClass = self.classes.currentItem().name
            self.files.currentItem().setSelected(False)


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


class OtherLoop(QRunnable, QObject):
    loop = Signal()

    def __init__(self, n: MainWindow):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.n = n
        self.running = True

    def run(self):
        while self.running:
            self.n.send_line_output()
            if self.n.files.currentItem() is not None:
                self.n.annotator.image = self.n.files.currentItem().name
                self.n.annotator.changeImage()
                if self.n.classes.currentItem() is not None:
                    self.n.annotator.activeClass = self.n.classes.currentItem().name
                self.n.files.currentItem().setSelected(False)
            time.sleep(.1)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = MainWindow()

    widget.show()
    widget.getactions()
    # ALL Signals below this comment

    widget.runner.getWidgets.connect(widget.getActive)
    widget.runner2.loop.connect(widget.loop)
    if app.exit():
        widget.runner.stop()
    sys.exit(app.exec())
