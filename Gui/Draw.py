import time

from PySide6.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QGridLayout
from PySide6.QtCore import QThread, Qt, Signal, Slot, QSize, QLine, QPoint
from PySide6.QtGui import QImage, QPixmap, QColor, QPainter


class Draw(QWidget):
    def __init__(self, a):
        super().__init__(a)
        self.last_y = None
        self.last_x = None
        self.window = a
        self.x = 640
        self.y = 640
        self.label = QLabel(a)
        self.canvas = QPixmap(self.size()).scaled(QSize(self.x, self.y))
        self.canvas.fill(QColor(255, 255, 255, 0))
        self.label.setPixmap(self.canvas)
        self.title = 'Annotator'
        self.activeClass = None
        self.mode = 'Poly'
        self.layout = QGridLayout()

        self.initUI()
        self.click = 0
        self.cords = []
        self.pair = []
        self.finished_annots = []
        self.full_cords = []
        self.loaded_anns = []
        self.prev_anns = []

    def setMode(self, mode):
        self.mode = mode
        print(self.activeClass)
        # self.clearCanvas()
        # self.deleteAllAnnotations()

    def mousePressEvent(self, e):
        if self.mode == 'poly':
            p1 = QPoint((e.position().x()) - 8 / 1, (e.position().y()) -2/ 1)
            print((QPoint(e.position().x(), e.position().y())).toTuple())
            self.cords.append(p1)
            self.updateCanvas()
            time.sleep(.1)
        elif self.mode == 'box':
            p1 = QPoint((e.position().x()) - 8 / 1, (e.position().y()) - 2 / 1)
            self.cords.append(p1)

    def get_box_points(self, orgin: QPoint, mouse_pos):
        x_orgin = orgin.x()
        y_orgin = orgin.y()
        x_mouse = mouse_pos.x() - 8
        y_mouse = mouse_pos.y() - 2
        b1 = orgin
        b2 = QPoint(x_mouse, y_orgin)
        b3 = QPoint(x_mouse, y_mouse)
        b4 = QPoint(x_orgin, y_mouse)
        self.cords = [b1, b2, b3, b4, b1]

    def mouseMoveEvent(self, event):
        if self.mode == 'poly':
            pass
        if self.mode == 'box':
            orgin = self.cords[0]
            self.full_cords = self.cords
            self.cords = []
            self.partialClear()
            self.get_box_points(orgin, event)
            self.updateCanvas()
            print(self.full_cords)

    # def mouseReleaseEvent(self, event):
    # if self.mode == 'box':
    # self.new_ann()
    # else:
    # return None

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
        self.canvas = QPixmap(self.size()).scaled(QSize(self.x, self.y))
        self.canvas.fill(QColor(255, 255, 255, 0))
        self.label.setPixmap(self.canvas)

    def deleteAllAnnotations(self):
        self.label.clear()
        self.cords = []
        self.finished_annots = []
        self.prev_anns = []
        self.pair = []
        self.canvas = QPixmap(self.size()).scaled(QSize(self.x, self.y))
        self.canvas.fill(QColor(255, 255, 255, 0))
        self.label.setPixmap(self.canvas)

    def clearLastAnnotation(self):
        self.finished_annots.pop()
        self.pair = []
        self.canvas = QPixmap(self.size()).scaled(QSize(self.x, self.y))
        self.canvas.fill(QColor(255, 255, 255, 0))
        self.label.setPixmap(self.canvas)

    def partialClear(self):
        self.label.clear()
        self.cords = []
        self.pair = []
        self.canvas = QPixmap(self.size()).scaled(QSize(self.x, self.y))
        self.canvas.fill(QColor(255, 255, 255, 0))
        self.label.setPixmap(self.canvas)

    def undo(self):
        if self.mode == 'poly':
            if self.cords:
                self.cords.pop()
                if len(self.cords) == 1:
                    self.cords.pop()
                self.label.clear()
                self.canvas = QPixmap(self.size()).scaled(QSize(self.x, self.y))
                self.canvas.fill(QColor(255, 255, 255, 0))
                self.label.setPixmap(self.canvas)
                self.updateCanvas()
        else:
            if self.cords:
                for i in range(5):
                    self.cords.pop()
                self.label.clear()
                self.canvas = QPixmap(self.size()).scaled(QSize(self.x, self.y))
                self.canvas.fill(QColor(255, 255, 255, 0))
                self.label.setPixmap(self.canvas)
                self.updateCanvas()

    def new_ann(self):
        print(self.cords)
        if self.cords:
            lst_str = f'{self.activeClass} '
            self.prev_anns.append(self.cords)
            for i in self.cords:
                lst_str += f'{((i.x() + 8) / 640)} '
                lst_str += f'{(i.y() +2 / 640)} '
            self.finished_annots.append(lst_str)
            self.cords = []

    def finish(self):
        if not self.cords:
            self.cords = self.full_cords
        self.full_cords = []
        if self.cords:
            if self.activeClass is not None:
                lst_str = f'{self.activeClass} '
            else:
                lst_str = ''
            for i in self.cords:
                lst_str += f'{((i.x() + 8) / 640)} '
                lst_str += f'{(i.y() +2 / 640)} '
            if self.mode == 'poly':
                lst_str += f'{(self.cords[0].x() + 8) / 640} '
                lst_str += f'{self.cords[0].y() + 2/ 640} '
            self.finished_annots.append(lst_str)
            a = self.finished_annots
            self.finished_annots = []
            self.prev_anns = []
            return a
        else:
            self.finished_annots = []
            self.prev_anns = []
            if self.mode == 'classification':
                if self.activeClass:
                    return f'{self.activeClass}'
                else:
                    return ''
            else:
                return ''
