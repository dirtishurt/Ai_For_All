# This Python file uses the following encoding: utf-8
import os
import shutil
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
        self.dialog = QFileDialog()
        self.workingDirectory = None
        self.dialog.setFileMode(QFileDialog.FileMode.Directory)
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
        self.ui.Next.clicked.connect(self.next)
        self.ui.Prev.clicked.connect(self.prev)
        self.ui.New_Ann.clicked.connect(self.new_ann)
        self.ui.menuOpen_Images.actions()[0].triggered.connect(self.fileSelectorDialog1)
        self.ui.menuOpen_Images.actions()[1].triggered.connect(self.fileSelectorDialog2)
        self.ui.menuSet_Project_Directory.actions()[0].triggered.connect(self.setWorkingDirectory)
        self.ui.menuView.actions()[0].triggered.connect(self.viewWorkingDirectory)
        self.ui.menuSave.actions()[0].triggered.connect(self.SaveAll)

    @Slot()
    def setWorkingDirectory(self):
        if self.dialog.exec():
            self.workingDirectory = self.dialog.selectedFiles()
        print(self.workingDirectory)

    @Slot()
    def SaveAll(self):
        pass

    @Slot()
    def viewWorkingDirectory(self):
        os.system(f'start {os.path.realpath(self.workingDirectory[0])}')

    def keyPressEvent(self, event):
        self.last_key = event.key()

    @Slot()
    def fileSelectorDialog1(self):
        print(self.ui.menuOpen_Images.actions())
        self.files.getFiles(1)

    @Slot()
    def fileSelectorDialog2(self):
        print(self.ui.menuOpen_Images.actions())
        self.files.getFiles(2)

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
                self.lastActive = self.active
                if self.active is not None:
                    self.active.toggle()
                self.active = i
            if self.active.text() == 'delete':
                self.active.toggle()
                self.draw.clearCanvas()
                if self.lastActive is not None:
                    self.active = self.lastActive
                    self.active.toggle()

            if self.active.text() == 'Undo':
                self.active.toggle()
                self.draw.undo()
                if self.lastActive is not None:
                    self.active = self.lastActive
                    self.active.toggle()

    @Slot()
    def prev(self):
        self.files.prev()

    @Slot()
    def next(self):
        self.files.next()
        a = self.draw.finish()
        print(a)
        if self.draw.activeClass is not None:
            filename = self.annotator.image.base[:len(self.annotator.image.base)-4] + '.txt'
            imgdir = self.annotator.image.name[:len(self.annotator.image.name)-len(self.annotator.image.base)]
            print(imgdir)
            print(filename)
            print(self.workingDirectory[0])
            if self.workingDirectory is not None:
                lbl_dir = os.path.join(self.workingDirectory[0], 'labels')
                cp_img_dir = os.path.join(self.workingDirectory[0], 'images')
                if os.path.exists(os.path.join(lbl_dir, filename)):
                    with open(os.path.join(lbl_dir, filename), 'a') as fn:
                        for _ in a:
                            fn.write(_)
                            fn.write('\n')
                        fn.close()
                else:
                    if os.path.exists(lbl_dir):
                        with open(os.path.join(lbl_dir, filename), 'x') as fn:
                            for _ in a:
                                fn.write(_)
                                fn.write('\n')
                            fn.close()
                    else:
                        os.mkdir(lbl_dir)
                        with open(os.path.join(lbl_dir, filename), 'x') as fn:
                            for _ in a:
                                fn.write(_)
                                fn.write('\n')
                            fn.close()
                if os.path.exists(cp_img_dir):
                    shutil.copy((imgdir+self.annotator.image.base), cp_img_dir)
                else:
                    os.mkdir(cp_img_dir)
                    shutil.copy((imgdir+self.annotator.image.base), cp_img_dir)
        self.draw.partialClear()

    @Slot()
    def new_ann(self):
        self.draw.new_ann()


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
                    time.sleep(.01)

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
                self.n.files.ref = self.n.files.currentItem()
                self.n.annotator.image = self.n.files.currentItem()
                self.n.annotator.changeImage()
                self.n.files.currentItem().setSelected(False)
            if self.n.classes.currentItem() is not None:
                self.n.annotator.activeClass = self.n.classes.currentItem().name
                self.n.draw.activeClass = self.n.classes.indexFromItem(self.n.classes.currentItem()).row()
            elif self.n.classes.currentItem() is None:
                self.n.annotator.activeClass = None
                self.n.draw.activeClass = None
            time.sleep(.1)


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
