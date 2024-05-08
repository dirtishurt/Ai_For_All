from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QWidgetAction, QFileDialog, QWidget
import PySide6.QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction, QKeyEvent, QColor, QPixmap
from PySide6.QtCore import QThread, QObject, QRunnable, QThreadPool, Signal, Slot, Qt, QEvent, QSize, QPoint

from ui_settings import Ui_Form
import time


class Settings(QWidget):
    emit_settings = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.last_key = None
        self.epochs = self.ui.lineEdit
        self.patience = self.ui.lineEdit_2

        self.epochs_n = 100
        self.patience_n = 20
        self.runner = OtherLoop(self)
        self.ui.pushButton.clicked.connect(self.save)

    def show_self(self):
        self.show()
        self.getactions()

    def keyPressEvent(self, event):
        self.last_key = event.key()
        print(self.patience_n, self.epochs_n)

    def send_line_output(self):
        if self.epochs.editingFinished:
            if self.last_key == Qt.Key.Key_Return:
                try:
                    self.epochs_n = int(self.epochs.text())
                except ValueError:
                    print("error")
        if self.patience.editingFinished:
            if self.last_key == Qt.Key.Key_Return:
                try:
                    self.patience_n = int(self.patience.text())
                except ValueError:
                    print("error")
            if self.patience_n > self.epochs_n:
                self.patience_n = self.epochs_n
        self.last_key = None

    @Slot()
    def save(self):
        self.runner.pause()
        self.hide()
        self.emit_settings.emit()

    def getactions(self):
        # threadCount = QThreadPool.globalInstance().maxThreadCount()
        pool = QThreadPool.globalInstance()

        self.runner = OtherLoop(self)
        pool.start(self.runner)



class OtherLoop(QRunnable, QObject):
    loop = Signal()

    def __init__(self, n: Settings):
        QObject.__init__(self)
        QRunnable.__init__(self)
        self.n = n
        self.running = True

    def run(self):
        while self.running:
            self.n.send_line_output()
            time.sleep(.1)

    def pause(self):
        self.running = False

    def unpause(self):
        self.running = True