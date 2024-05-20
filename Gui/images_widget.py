# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'images.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLineEdit, QListWidget, QListWidgetItem,
    QSizePolicy, QWidget)

from Display import Display

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(920, 722)
        Form.setMaximumSize(QSize(920, 722))
        self.Images = QListWidget(Form)
        self.Images.setObjectName(u"Images")
        self.Images.setGeometry(QRect(660, 10, 241, 681))
        self.Preview = Display(Form)
        self.Preview.setObjectName(u"Preview")
        self.Preview.setGeometry(QRect(20, 10, 640, 640))
        palette = QPalette()
        brush = QBrush(QColor(62, 180, 137, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.Preview.setPalette(palette)
        self.Preview.setAutoFillBackground(True)
        self.Search = QLineEdit(Form)
        self.Search.setObjectName(u"Search")
        self.Search.setGeometry(QRect(20, 650, 641, 41))
        self.AMount = QLineEdit(Form)
        self.AMount.setObjectName(u"AMount")
        self.AMount.setGeometry(QRect(20, 690, 171, 21))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Search For Images", None))
        self.Search.setPlaceholderText(QCoreApplication.translate("Form", u"Search:", None))
        self.AMount.setPlaceholderText(QCoreApplication.translate("Form", u"Amount:", None))
    # retranslateUi

