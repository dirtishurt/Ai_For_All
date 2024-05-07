import math
import os
import time

import ultralytics.utils.callbacks.wb
from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidgetAction, QFileDialog, QWidget
import PySide6.QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction, QKeyEvent, QColor, QPixmap
from PySide6.QtCore import QThread, QObject, QRunnable, QThreadPool, Signal, Slot, Qt, QEvent, QSize, QPoint
from threading import Thread

import project_utils
from ui_train import Ui_Train
import settings_widget
import torch
from ultralytics import YOLO

import multiprocessing
import subprocess
from train import runTrain


class Train(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Train()
        self.ui.setupUi(self)
        self.settings = settings_widget.Settings()
        self.dataset_selector = self.ui.select_dataset
        self.model_selector = self.ui.select_model
        self.settings.emit_settings.connect(self.get_settings)
        self.ui.Settings.clicked.connect(self.show_settings)

        self.progress = self.ui.progressBar
        self.workingDirectory = None
        self.epochs = 20
        self.patience = 0
        self.dataset_list = []
        self.models = []
        self.model = None
        self.dataset = None
        self.runner = None
        self.pool = QThreadPool.globalInstance()

        self.ui.Train_2.clicked.connect(self.start)

    @Slot()
    def show_settings(self):
        self.settings.show_self()
        if not self.settings.runner.running:
            self.settings.runner.unpause()

    def add_datasets(self, directory):
        for i in os.listdir(directory):
            if i[0:7] == 'dataset':
                for z in os.listdir(os.path.join(directory, i)):
                    if z == 'data.yaml':
                        print(i)
                        x = Item(os.path.join(os.path.join(directory, i), z), i)
                        self.dataset_list.append(x)
                        self.dataset_selector.addItem(x.name)
        self.add_models()

    @Slot()
    def start(self):
        self.ui.Train_2.setDisabled(True)
        self.check_selected()
        if os.path.exists(os.path.join(self.workingDirectory, 'runs')):
            pass
        else:
            os.mkdir(os.path.join(self.workingDirectory, 'runs'))
        export_path = os.path.join(self.workingDirectory, 'runs')

        if self.model:
            if self.dataset:
                # subprocess.call(['python.exe', '.\\train-script.py', str([str(self.dataset.path), str(self.patience),str(self.epochs),str(export_path),str(self.model.path)])])
                self.runner = workerThread(self)
                self.runner.start()
                print('balls')
        self.ui.Train_2.setDisabled(False)

    def check_selected(self):
        if self.model_selector.currentIndex() >= 0:
            self.model = self.models[self.model_selector.currentIndex()]
        if self.dataset_selector.currentIndex() >= 0:
            self.dataset = self.dataset_list[self.dataset_selector.currentIndex()]

    def add_models(self):
        # Check for errors
        current = os.getcwd()
        os.chdir('..')
        os.chdir('..')
        path = os.path.abspath('./Working_Models/base-ultralytics')
        for i in os.listdir(path):
            x = Item(os.path.join(path, i), i)
            self.models.append(x)
            self.model_selector.addItem(x.name)
        os.chdir(current)

    @Slot()
    def get_settings(self):
        self.patience = self.settings.patience_n
        self.epochs = self.settings.epochs_n
        # print(self.patience, self.epochs, 'Train Settings')


class Item:

    def __init__(self, path, name):
        self.name = name
        self.path = path


class workerThread(QThread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.e = 0
        self.model = YOLO(self.parent.model.path)

        self.model.add_callback('on_train_epoch_end', self.on_epoch_end)
        self.model.add_callback('on_train_start', self.train_start)
        #self.model.add_callback('on_train_epoch_start', self.on_train_epoch_end)
        self.model.add_callback('on_train_end', self.on_train_end)

    def on_epoch_end(self, epoch, logs=None):
        self.e += 1
        print(self.e)
        self.parent.progress.setValue((self.e/self.parent.epochs)*100)

    def train_start(self, epoch):
        self.parent.progress.setValue(0)



    def on_train_end(self, epochs, logs=None):
        self.parent.progress.setValue(100)

    def run(self):
        e = 0
        if os.path.exists(os.path.join(self.parent.workingDirectory, 'runs')):
            pass
        else:
            os.mkdir(os.path.join(self.parent.workingDirectory, 'runs'))
        export_path = os.path.join(self.parent.workingDirectory, 'runs')

        if torch.cuda.is_available():
            print('CUDA Compatible Detected, Starting Training')
            self.model.train(data=self.parent.dataset.path, device=0, patience=self.parent.patience,
                             epochs=self.parent.epochs,
                             imgsz=640, project=export_path, verbose=False)

        else:
            print('WARNING CUDA COMPATIBLE GPU NOT DETECTED, TRAINING WILL TAKE LONGER...')
            self.model.train(data=self.parent.dataset.path, device='cpu', patience=self.parent.patience,
                             epochs=self.parent.epochs,
                             imgsz=640, project=export_path, verbose=False)


