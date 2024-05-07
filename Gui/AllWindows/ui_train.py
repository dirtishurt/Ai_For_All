# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'train.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QProgressBar, QPushButton,
    QSizePolicy, QWidget)

class Ui_Train(object):
    def setupUi(self, Train):
        if not Train.objectName():
            Train.setObjectName(u"Train")
        Train.resize(581, 257)
        self.progressBar = QProgressBar(Train)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(0, 200, 581, 23))
        palette = QPalette()
        brush = QBrush(QColor(62, 180, 137, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        palette.setBrush(QPalette.Active, QPalette.Link, brush)
        palette.setBrush(QPalette.Active, QPalette.Accent, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Link, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Accent, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Accent, brush)
        self.progressBar.setPalette(palette)
        self.progressBar.setAutoFillBackground(True)
        self.progressBar.setValue(0)
        self.progressBar.setInvertedAppearance(False)
        self.Train_2 = QPushButton(Train)
        self.Train_2.setObjectName(u"Train_2")
        self.Train_2.setGeometry(QRect(430, 0, 151, 101))
        self.select_dataset = QComboBox(Train)
        self.select_dataset.setObjectName(u"select_dataset")
        self.select_dataset.setGeometry(QRect(150, 0, 281, 51))
        self.Settings = QPushButton(Train)
        self.Settings.setObjectName(u"Settings")
        self.Settings.setGeometry(QRect(0, 0, 151, 101))
        self.select_model = QComboBox(Train)
        self.select_model.setObjectName(u"select_model")
        self.select_model.setGeometry(QRect(150, 50, 281, 51))

        self.retranslateUi(Train)

        QMetaObject.connectSlotsByName(Train)
    # setupUi

    def retranslateUi(self, Train):
        Train.setWindowTitle(QCoreApplication.translate("Train", u"Train Model", None))
        self.Train_2.setText(QCoreApplication.translate("Train", u"Train!", None))
        self.select_dataset.setCurrentText("")
        self.select_dataset.setPlaceholderText(QCoreApplication.translate("Train", u"Select Dataset", None))
        self.Settings.setText(QCoreApplication.translate("Train", u"Settings", None))
        self.select_model.setCurrentText("")
        self.select_model.setPlaceholderText(QCoreApplication.translate("Train", u"Select Model", None))
    # retranslateUi

