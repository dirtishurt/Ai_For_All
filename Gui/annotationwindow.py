# This Python file uses the following encoding: utf-8
import math
import os
import random
import shutil
import sys
import time

import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidgetAction, QFileDialog, QWidget
import PySide6.QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction, QKeyEvent, QColor, QPixmap
from PySide6.QtCore import QThread, QObject, QRunnable, QThreadPool, Signal, Slot, Qt, QEvent, QSize, QPoint

try:
    import Id_Recognition.project_utils
except:
    import project_utils
# Important:
# You need to run the following command to generate the ui_form2.py file
#     pyside6-uic form2.ui -o ui_form2.py, or
#     pyside2-uic form2.ui -o ui_form2.py
from ui_form2 import Ui_MainWindow as ui

try:
    from Id_Recognition.project_utils import resize_img, partition_pct
except:
    from project_utils import resize_img, partition_pct


class MainWindow(QMainWindow):
    keysPressed = Signal(QEvent)

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.dialog = QFileDialog(caption='Set Project Directory')
        self.workingDirectory = None
        self.dialog.setFileMode(QFileDialog.FileMode.Directory)
        self.last_key = None
        self.file_path = None
        self.ui = ui()
        self.ui.setupUi(self)
        self.toolbar = self.ui.toolBar
        self.runner = None
        self.runner2 = None
        self.imgsAdd = self.ui.menuOpen_Images
        self.active = None
        self.lastActive = None
        self.lineedit = self.ui.lineEdit
        self.pool = QThreadPool.globalInstance()

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
        self.ui.menuCreate_Training_Set.actions()[0].triggered.connect(self.create_set)
        self.setWindowState(QMainWindow.windowState(self).WindowMaximized)
        # self.ui.menuTest.actions()[0].triggered.connect(self.show())

        self.lastFile = None

        self.draw.setMode('poly')
        self.files.itemClicked.connect(self.get_selected)

    def load_images(self):
        if self.workingDirectory:
            if os.path.exists(os.path.join(self.workingDirectory[0], 'image_paths.txt')):
                path = os.path.join(self.workingDirectory[0], 'image_paths.txt')
                if os.path.exists(path):
                    file = open(path, 'r')
                    c = []
                    for line in file:
                        if line != '':
                            c.append(line.removesuffix('\n'))
                    for i in c:
                        self.files.filenames = [i]
                        self.files.printfilenames()
                    file.close()


    @Slot()
    def setWorkingDirectory(self):
        self.opening = True
        if self.dialog.exec():
            self.workingDirectory = self.dialog.selectedFiles()
            self.load_images()

        self.classes.load_classes(self.workingDirectory[0])
    @Slot()
    def return_to_main(self):
        self.hide()


    @Slot()
    def show_self(self):
        if self.workingDirectory:
            self.classes.load_classes(self.workingDirectory[0])
            self.load_images()
        self.showFullScreen()

    @Slot()
    def SaveAll(self):
        self.classes.save_classes(self.workingDirectory[0])
        #self.files.save_image_paths(self.workingDirectory[0])
    @Slot()
    def viewWorkingDirectory(self):
        if self.workingDirectory is not None:
            os.system(f'start {os.path.realpath(self.workingDirectory[0])}')

    def keyPressEvent(self, event):
        self.last_key = event.key()

    @Slot()
    def fileSelectorDialog1(self):
        print(self.ui.menuOpen_Images.actions())
        self.files.getFiles(1, self.workingDirectory[0])

    @Slot()
    def fileSelectorDialog2(self):
        print(self.ui.menuOpen_Images.actions())
        self.files.getFiles(2, self.workingDirectory[0])

    def send_line_output(self):
        if self.lineedit.editingFinished:
            if self.last_key == Qt.Key.Key_Return:
                if self.lineedit.text() not in self.classes.classes:
                    if self.lineedit.text() is not None:
                        self.classes.classes.append(self.lineedit.text())
                        self.classes.add_classes()
                        self.classes.setCurrentItem(self.classes.item(len(self.classes.classes) - 1))
                        self.classes.currentItem().setSelected(True)
                        print(self.classes.currentItem().isSelected())
                self.lineedit.clear()
                self.last_key = None

    def getactions(self):
        # threadCount = QThreadPool.globalInstance().maxThreadCount()

        self.runner = Runnable(self.toolbar.actions())
        self.runner2 = OtherLoop(self)
        self.pool.start(self.runner)
        self.pool.start(self.runner2)

    @Slot(QAction)
    def getActive(self, i):
        if i.isChecked():
            if self.active != i:
                self.lastActive = self.active

                if self.active is not None:

                    if i.text() == 'Box':
                        self.draw.setMode('box')
                    if i.text() == 'PolygonTool':
                        self.draw.setMode('poly')
                    self.active.toggle()
                self.active = i
            if self.active.text() == 'delete':
                self.annotator.image = self.files.currentItem()
                filename = self.annotator.image.base[:len(self.annotator.image.base) - 4] + '.txt'
                lbl_dir = os.path.join(self.workingDirectory[0], 'labels')
                if os.path.exists(os.path.join(lbl_dir, filename)):
                    file = open(os.path.join(lbl_dir, filename), 'w')
                    file.write('')
                    file.close()
                self.active.toggle()
                self.draw.deleteAllAnnotations()
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
        if self.workingDirectory is not None:
            a = self.draw.finish()

            lbl_dir = os.path.join(self.workingDirectory[0], 'labels')
            cp_img_dir = os.path.join(self.workingDirectory[0], 'images')

            if self.annotator.image is not None:
                filename = self.annotator.image.base[:len(self.annotator.image.base) - 4] + '.txt'
                imgdir = self.annotator.image.name[:len(self.annotator.image.name) - len(self.annotator.image.base)]
                if self.workingDirectory is not None:
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
                        i = resize_img((imgdir + self.annotator.image.base))
                        cv2.imwrite(f'{cp_img_dir}/{self.annotator.image.base}', i)
                    else:
                        os.mkdir(cp_img_dir)
                        i = resize_img((imgdir + self.annotator.image.base))
                        cv2.imwrite(f'{cp_img_dir}/{self.annotator.image.base}', i)
            self.draw.clearCanvas()
            self.files.prev()
            self.files.ref = self.files.currentItem()
            self.annotator.image = self.files.currentItem()
            self.annotator.changeImage()
            self.files.currentItem().setSelected(False)
            self.getPrev(lbl_dir)

    @Slot()
    def next(self):
        if self.workingDirectory is not None:
            a = self.draw.finish()

            lbl_dir = os.path.join(self.workingDirectory[0], 'labels')
            cp_img_dir = os.path.join(self.workingDirectory[0], 'images')

            if self.annotator.image is not None:
                filename = self.annotator.image.base[:len(self.annotator.image.base) - 4] + '.txt'
                imgdir = self.annotator.image.name[:len(self.annotator.image.name) - len(self.annotator.image.base)]
                if self.workingDirectory is not None:
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
                        i = resize_img((imgdir + self.annotator.image.base))
                        cv2.imwrite(f'{cp_img_dir}/{self.annotator.image.base}', i)
                    else:
                        os.mkdir(cp_img_dir)
                        i = resize_img((imgdir + self.annotator.image.base))
                        cv2.imwrite(f'{cp_img_dir}/{self.annotator.image.base}', i)
            self.draw.clearCanvas()
            self.files.next()
            self.files.ref = self.files.currentItem()
            self.annotator.image = self.files.currentItem()
            self.annotator.changeImage()
            self.files.currentItem().setSelected(False)
            self.getPrev(lbl_dir)
    @Slot()
    def get_selected(self):
        if self.workingDirectory is not None:
            a = self.draw.finish()
            lbl_dir = os.path.join(self.workingDirectory[0], 'labels')
            cp_img_dir = os.path.join(self.workingDirectory[0], 'images')

            if self.annotator.image is not None:
                filename = self.annotator.image.base[:len(self.annotator.image.base) - 4] + '.txt'
                imgdir = self.annotator.image.name[:len(self.annotator.image.name) - len(self.annotator.image.base)]
                if self.workingDirectory is not None:
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
                        i = resize_img((imgdir + self.annotator.image.base))
                        cv2.imwrite(f'{cp_img_dir}/{self.annotator.image.base}', i)
                    else:
                        os.mkdir(cp_img_dir)
                        i = resize_img((imgdir + self.annotator.image.base))
                        cv2.imwrite(f'{cp_img_dir}/{self.annotator.image.base}', i)
            self.draw.clearCanvas()
            self.files.ref = self.files.currentItem()
            self.annotator.image = self.files.currentItem()
            self.annotator.changeImage()
            self.files.currentItem().setSelected(False)
            self.getPrev(lbl_dir)


    def getPrev(self, lbl_dir):
        self.classes.save_classes(self.workingDirectory[0])
        self.annotator.image = self.files.currentItem()
        filename = self.annotator.image.base[:len(self.annotator.image.base) - 4] + '.txt'
        if os.path.exists(os.path.join(lbl_dir, filename)):
            print(os.path.join(lbl_dir, filename))
            file = open(os.path.join(lbl_dir, filename), 'r')
            c = []
            for line in file:
                if line != '':
                    c.append(line.removesuffix('\n'))
            file.close()

            # Remove the class header
            for o in range(len(c)):
                for i in c[o]:
                    x = ''
                    if i != '.':
                        if i == ' ':
                            b = o
                            print((c[b])[len(x) + 2:])
                            c.__setitem__(b, c[b][len(x) + 2:])
                            break
                        else:
                            x += i
                    else:
                        break
            # Draw the loaded annotations
            listlist = []
            pairtag = []
            pcount = 0
            x = ''
            for o in c:
                for i in o:
                    if i == " ":
                        pairtag.append(x)
                        pcount += 1
                        if pcount == 2:
                            listlist.append(pairtag)
                            pairtag = []
                            pcount = 0
                        x = ''
                    else:
                        x += i
            points = []
            f = None
            f_c = 0
            set_f = 1
            for i in listlist:
                if set_f == 1:
                    f = i
                    set_f = 0
                x = int(float(i[0]) * 640) - 9
                y = int(float(i[1]) * 640)
                points.append(QPoint(x, y))
                if i == f:
                    f_c += 1
                    if f_c == 2:
                        set_f = 1
                        f_c = 0
                        self.draw.prev_anns.append(points)
                        points = []
            self.draw.updateCanvas()

    @Slot()
    def create_set(self):
        if self.workingDirectory[0] is not None:
            img_path = os.path.join(self.workingDirectory[0], 'images')
            lbl_path = os.path.join(self.workingDirectory[0], 'labels')
            train_img_list, p_30 = partition_pct(os.listdir(img_path), .7)
            valid_img_list, test_img_list = partition_pct(p_30, .666)
            print(train_img_list, test_img_list, valid_img_list)
            name = project_utils.getRandomName()
            datasetdir = os.path.join(self.workingDirectory[0], f'dataset_{name}')
            os.mkdir(datasetdir)
            os.mkdir(os.path.join(datasetdir, 'train'))
            os.mkdir(os.path.join(datasetdir, 'train/images'))
            os.mkdir(os.path.join(datasetdir, 'train/labels'))
            os.mkdir(os.path.join(datasetdir, 'valid'))
            os.mkdir(os.path.join(datasetdir, 'valid/images'))
            os.mkdir(os.path.join(datasetdir, 'valid/labels'))
            os.mkdir(os.path.join(datasetdir, 'test'))
            os.mkdir(os.path.join(datasetdir, 'test/images'))
            os.mkdir(os.path.join(datasetdir, 'test/labels'))
            for i in os.listdir(lbl_path):
                name = ''
                for x in i:
                    if x == '.':
                        print(name)
                        break
                    else:
                        name += x
                print(f'{name}.txt')

                for o in train_img_list:
                    if f'{name}' == o.removesuffix('.jpg'):
                        shutil.copy(os.path.join(img_path, f'{name}.jpg'), os.path.join(datasetdir, 'train/images'))
                        shutil.copy(os.path.join(lbl_path, f'{name}.txt'), os.path.join(datasetdir, 'train/labels'))
                for o in test_img_list:
                    if f'{name}' == o.removesuffix('.jpg'):
                        shutil.copy(os.path.join(img_path, f'{name}.jpg'), os.path.join(datasetdir, 'test/images'))
                        shutil.copy(os.path.join(lbl_path, f'{name}.txt'), os.path.join(datasetdir, 'test/labels'))
                for o in valid_img_list:
                    if f'{name}' == o.removesuffix('.jpg'):
                        shutil.copy(os.path.join(img_path, f'{name}.jpg'), os.path.join(datasetdir, 'valid/images'))
                        shutil.copy(os.path.join(lbl_path, f'{name}.txt'), os.path.join(datasetdir, 'valid/labels'))
            self.create_yaml(datasetdir)

    def create_yaml(self, datasetdir):
        path = os.path.join(datasetdir, 'data.yaml')
        file = open(path, 'w')
        file.write('train: ./train/images\n')
        file.write('val: ./valid/images\n')
        file.write('test: ./test/images\n')
        file.write('\n')
        file.write(f'nc: {len(self.classes.classes)}\n')
        file.write(f'names: {self.classes.classes}')

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
        del self


class OtherLoop(QRunnable, QObject):
    loop = Signal()

    def __init__(self, n: MainWindow):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.n = n
        self.running = True

    def run(self):
        while self.running:
            if self.n.files:
                self.n.send_line_output()
                #if self.n.files.currentItem() is not None:
                #    if self.n.files.open:
                 #       self.n.files.ref = self.n.files.currentItem()
                #        self.n.annotator.image = self.n.files.currentItem()
                #        self.n.annotator.changeImage()
                 #       self.n.files.currentItem().setSelected(False)
                if self.n.classes.currentItem() is not None:
                    self.n.annotator.activeClass = self.n.classes.currentItem().name
                    self.n.draw.activeClass = self.n.classes.indexFromItem(self.n.classes.currentItem()).row()
                elif self.n.classes.currentItem() is None:
                    self.n.annotator.activeClass = None
                    self.n.draw.activeClass = None
            time.sleep(.1)

    def stop(self):
        self.running = False
        del self
