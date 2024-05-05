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
        self.loaded_anns = []
        self.prev_anns = []

    def mousePressEvent(self, e):

        p1 = QPoint((e.position().x()) - 9 / 1, (e.position().y()) / 1)
        self.cords.append(p1)
        self.updateCanvas()
        time.sleep(.1)

    def updateCanvas(self):
        if self.cords or self.prev_anns:
            canvas = self.label.pixmap()
            painter = QPainter(canvas)
            painter.pen().setWidth(3)
            if self.cords:
                painter.drawPolyline(self.cords)
            if self.prev_anns:
                for i in self.prev_anns:
                    painter.drawPolyline(i)
            # painter.drawPolyline(self.finished_annots)
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

    def deleteAllAnnotations(self):
        self.label.clear()
        self.cords = []
        self.finished_annots = []
        self.pair = []
        self.canvas = QPixmap(self.window.size()).scaled(QSize(640, 640))
        self.canvas.fill(QColor(255, 255, 255, 0))
        self.label.setPixmap(self.canvas)

    def clearLastAnnotation(self):
        self.finished_annots.pop()
        self.pair = []
        self.canvas = QPixmap(self.window.size()).scaled(QSize(640, 640))
        self.canvas.fill(QColor(255, 255, 255, 0))
        self.label.setPixmap(self.canvas)

    def partialClear(self):
        self.label.clear()
        self.cords = []
        self.pair = []
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

    def new_ann(self):
        if self.cords:
            lst_str = f'{self.activeClass} '
            self.prev_anns.append(self.cords)
            for i in self.cords:
                lst_str += f'{((i.x()+9) / 640)} '
                lst_str += f'{(i.y() / 640)} '
            self.finished_annots.append(lst_str)
            self.cords = []

    def finish(self):

        if self.cords:
            if self.activeClass is not None:
                lst_str = f'{self.activeClass} '
            else:
                lst_str = ''
            for i in self.cords:
                lst_str += f'{((i.x()+9) / 640)} '
                lst_str += f'{(i.y() / 640)} '
            lst_str += f'{(self.cords[0].x()+9) / 640} '
            lst_str += f'{self.cords[0].y() / 640} '
            self.finished_annots.append(lst_str)
            a = self.finished_annots
            self.finished_annots = []
            self.prev_anns = []
            return a
        else:
            self.finished_annots = []
            self.prev_anns = []
            return ''
