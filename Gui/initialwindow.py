# This Python file uses the following encoding: utf-8
import sys
import time

from imagesearchwidget import Image_Search
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QComboBox, QSizePolicy
from PySide6.QtCore import Signal, Slot, QRunnable, QObject, Qt, QThreadPool, QSize
from PySide6.QtGui import QBrush, QPalette, QColor
import webbrowser
from Camera import Camera

# Important:
# You need to run the following command to generate the ui_form2.py file
#     pyside6-uic form2.ui -o ui_form2.py, or
#     pyside2-uic form2.ui -o ui_form2.py
from Gui.ui_form import Ui_MainWindow as ui1
import os
import train_widget


class MainWindow(QMainWindow):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.file_path = None
        self.confidence = 5
        self.ui = ui1()
        self.ui.setupUi(self)
        self.menubar = self.ui.menubar
        self.ui.end_button.clicked.connect(self.stop)
        self.ui.run_button.clicked.connect(self.run)
        self.ui.confidence_slider.setMinimum(5)
        self.ui.confidence_slider.setMaximum(95)
        self.ui.confidence_slider.valueChanged.connect(self.confidence_value_changed)
        self.tw = train_widget.Train()
        self.model_selector = QComboBox()
        self.models = []
        self.imagesearch = Image_Search(ann=None)
        self.p_text = self.ui.confidence_percent
        self.p_text.setMaxLength(2)
        self.camera = self.ui.camer_output
        self.cn = self.ui.menuCreateModels.actions()[0]
        self.train = self.ui.menuCreateModels.actions()[1]
        self.train.triggered.connect(self.open_training_dialog)

        self.load_project = self.ui.menuLoad_Model.actions()[0]
        self.load_project.triggered.connect(self.setWorkingDirectory)
        self.dialog = QFileDialog(caption='Set Project Directory')
        self.workingDirectory = None
        self.dialog.setFileMode(QFileDialog.FileMode.Directory)
        self.file_path = None
        self.ui.menuImport_Model.actions()[0].triggered.connect(self.import_model)
        self.loaded_models = []
        self.ui.menuHelp.actions()[0].triggered.connect(self.help)
        self.model_selector.setPlaceholderText('Select Model')
        path = os.path.abspath('../Working_Models/base-ultralytics')
        for i in os.listdir(path):
            x = train_widget.Item(os.path.join(path, i), i)
            self.models.append(x)
            self.model_selector.addItem(x.name)


        # ALL Signals below this comment
        self.running = True
        self.last_key = None
        self.runner = None
        self.quitting = False
        self.app = app

        ####################
        a = QMessageBox(text='Thank you for using the program. Please set a project directory before doing anything'
                             'else.')
        a.exec()


    @Slot()
    def setWorkingDirectory(self):
        if self.dialog.exec():
            self.workingDirectory = self.dialog.selectedFiles()

        print(self.workingDirectory)
        ann = self.findChildren(QMainWindow, 'MainWindow')[0]
        ann.workingDirectory = self.workingDirectory
        self.tw.workingDirectory = self.workingDirectory[0]
        print(ann.workingDirectory)

    @Slot()
    def help(self):
        webbrowser.open('https://github.com/dirtishurt/Ai_For_All/blob/main/README.md')

    @Slot()
    def end(self):
        sys.exit()

    @Slot()
    def open_training_dialog(self):
        self.tw.show()
        self.tw.add_datasets(self.workingDirectory[0])

    @Slot()
    def open_image_search(self):
        ann = self.findChildren(QMainWindow, 'MainWindow')[0]
        ann.hide()
        self.imagesearch.show()
        self.imagesearch.workingDirectory = self.workingDirectory[0]
        self.imagesearch.showmethod()

    @Slot()
    def import_model(self):
        dl = QFileDialog(caption='Select .pt file')
        dl.setFileMode(QFileDialog.FileMode.ExistingFile)
        dl.setNameFilter('*.pt')
        if dl.exec():
            s_f = dl.selectedFiles()
            self.loaded_models.append(s_f)
            print(s_f)

    def close(self):
        os.system(f'.\\nircmd.exe setdisplay {str(self.screen_size.width)} {str(self.screen_size.height)} 32')

    def github(self):
        if self.ui.menuGithub.get_mouse_event():
            webbrowser.open("https://github.com/dirtishurt/Ai_For_All")

    def getactions(self):
        # threadCount = QThreadPool.globalInstance().maxThreadCount()
        pool = QThreadPool.globalInstance()

        self.runner = OtherLoop(self)
        pool.start(self.runner)

    def keyPressEvent(self, event):
        self.last_key = event.key()

    @Slot(QMainWindow)
    def create_new(self, other):
        self.hide()
        other.show()

    def show_self(self):
        self.show()
        self.setWindowState(QMainWindow.windowState(self).WindowFullScreen)

    def send_line_output(self):

        if self.p_text.editingFinished:
            if self.last_key == Qt.Key.Key_Return:
                try:
                    self.confidence = int(self.p_text.text())
                    self.ui.confidence_slider.setValue(self.confidence)
                except ValueError:
                    print("error")
            self.last_key = None

    @Slot()
    def run(self):
        self.model_selector.show()

    @Slot(int)
    def run_2(self, a):
        if a >= 0:
            print(self.models[self.model_selector.currentIndex()].path)
            self.model_selector.hide()
            self.camera.initUI(self.models[self.model_selector.currentIndex()].path,
                               self.ui.confidence_slider)

    # This just stops the camera by deleting it, and reinserting it.
    @Slot()
    def stop(self):
        if self.camera.th.isRunning:
            self.camera.th.isRunning = False
            self.ui.camer_output = Camera(self.ui.centralwidget)
            self.ui.camer_output.setObjectName(u"camer_output")
            sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
            sizePolicy1.setHorizontalStretch(0)
            sizePolicy1.setVerticalStretch(0)
            sizePolicy1.setHeightForWidth(self.ui.camer_output.sizePolicy().hasHeightForWidth())
            self.ui.camer_output.setSizePolicy(sizePolicy1)
            self.ui.camer_output.setMinimumSize(QSize(640, 360))
            self.ui.camer_output.setMaximumSize(QSize(2560, 1440))
            self.ui.camer_output.setSizeIncrement(QSize(16, 9))
            self.ui.camer_output.setBaseSize(QSize(16, 9))
            palette1 = QPalette()
            brush1 = QBrush(QColor(62, 180, 137, 255))
            brush1.setStyle(Qt.SolidPattern)
            palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
            palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
            palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
            palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
            self.ui.camer_output.setPalette(palette1)
            self.ui.camer_output.setAutoFillBackground(True)
            self.ui.verticalLayout.insertWidget(0, self.ui.camer_output)
            self.ui.run_button.clicked.connect(self.ui.camer_output.update)
            self.ui.end_button.clicked.connect(self.ui.camer_output.close)
            self.camera = self.ui.camer_output




    @Slot()
    def confidence_value_changed(self, value):
        self.confidence = value


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
            self.n.github()
            if self.n.model_selector.isVisible():
                self.n.model_selector.currentIndexChanged.connect(self.n.run_2(self.n.model_selector.currentIndex()
                                                                               ))
            time.sleep(.1)
