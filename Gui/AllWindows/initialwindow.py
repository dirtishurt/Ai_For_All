# This Python file uses the following encoding: utf-8
import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Signal, Slot, QRunnable, QObject, Qt, QThreadPool
import webbrowser

# Important:
# You need to run the following command to generate the ui_form2.py file
#     pyside6-uic form2.ui -o ui_form2.py, or
#     pyside2-uic form2.ui -o ui_form2.py
from Gui.AllWindows.ui_form import Ui_MainWindow as ui1




class MainWindow(QMainWindow):
    def __init__(self, parent=None):
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

        self.p_text = self.ui.confidence_percent
        self.p_text.setMaxLength(2)
        self.camera = self.ui.camer_output
        self.cn = self.ui.menuCreateModels.actions()[0]

        # ALL Signals below this comment
        self.running = True
        self.last_key = None
        self.runner = None

    @Slot()
    def end(self):
        sys.exit()

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

    @Slot()
    def create_new(self):
        self.hide()
        return True

    def show_self(self):
        self.show()





    def send_line_output(self):

        if self.p_text.editingFinished:
            if self.last_key == Qt.Key.Key_Return:
                self.confidence = int(self.p_text.text())
                self.ui.confidence_slider.setValue(self.confidence)
            self.last_key = None

    @Slot()
    def run(self):
        self.camera.initUI()

    @Slot()
    def stop(self):
        self.camera.exit()

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
            time.sleep(.1)


if __name__ == "__main__":
    print('a')
    app = QApplication(sys.argv)
    widget = MainWindow()


    widget.show()
    widget.getactions()
    sys.exit(app.exec())
