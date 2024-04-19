import cv2
from PySide6.QtWidgets import  QWidget, QLabel, QApplication
from PySide6.QtCore import QThread, Qt, Signal, Slot
from PySide6.QtGui import QImage, QPixmap
pyqtSignal = Signal
pyqtSlot = Slot
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def run(self):
        self.isRunning=True
        cap = cv2.VideoCapture(0)
        while self.isRunning:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def stop(self):
        self.isRunning=False
        self.quit()
        self.terminate()

class Camera(QWidget):
    def __init__(self, a):
        super().__init__()
        self.title = 'PySide Video'
        self.left = 0
        self.top = 0
        self.fwidth = 640
        self.fheight = 640
        self.initUI(a)
    @pyqtSlot(QImage)
    def setImage(self, image):
        #update image
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self, a):
        self.setGeometry(self.left, self.top, self.fwidth, self.fheight)
        self.resize(600, 600)

        # create a label
        self.label = QLabel(a)
        self.label.resize(200, 200)
        self.label.move(200,200)
        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

