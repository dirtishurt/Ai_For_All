import time

from PySide6.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout
from PySide6.QtCore import QThread, Qt, Signal, Slot, QSize, QLine, QPoint
from PySide6.QtGui import QImage, QPixmap, QColor, QPainter


class Draw(QWidget):
    def __init__(self, a):
        super().__init__(a)
        self.last_y = None
        self.last_x = None
        self.window = a
        self.label = QLabel(a)
        self.canvas = QPixmap(a.size()).scaled(QSize(640, 640))
        self.canvas.fill(QColor(255, 255, 255, 0))
        self.label.setPixmap(self.canvas)
        self.title = 'Annotator'
        self.activeClass = None

        self.layout = QVBoxLayout()
        self.initUI()
        self.click = 0
        self.cords = []
        self.pair = []
        self.finished_annots = []

    def mousePressEvent(self, e):

        p1 = QPoint((e.position().x()) - 8 / 1, (e.position().y()) / 1)
        self.cords.append(p1)
        self.updateCanvas()
        time.sleep(.1)

    def updateCanvas(self):
        if self.cords:
            canvas = self.label.pixmap()
            painter = QPainter(canvas)
            painter.drawPolyline(self.cords)
            painter.end()
            self.label.setPixmap(canvas)


    def initUI(self):
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

    def clearCanvas(self):
        self.label.clear()
        self.cords = []
        self.pair = []
        self.finished_annots = []
        self.canvas = QPixmap(self.window.size()).scaled(QSize(640, 640))
        self.canvas.fill(QColor(255, 255, 255, 0))
        self.label.setPixmap(self.canvas)

    def undo(self):
        if self.cords:
            self.cords.pop()
            if len(self.cords) == 1:
                self.cords.pop()
            self.label.clear()
            self.canvas = QPixmap(self.window.size()).scaled(QSize(640, 640))
            self.canvas.fill(QColor(255, 255, 255, 0))
            self.label.setPixmap(self.canvas)
            self.updateCanvas()

    def finish(self):
        if self.activeClass and self.cords:
            self.finished_annots.append((self.activeClass, self.cords, self.cords[0]))
            self.cords = []
            self.pair = []
            print(self.finished_annots)

