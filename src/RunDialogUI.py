# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RunDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QGraphicsView,
    QHBoxLayout, QPlainTextEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_RunDialog(object):
    def setupUi(self, RunDialog):
        if not RunDialog.objectName():
            RunDialog.setObjectName(u"RunDialog")
        RunDialog.resize(739, 402)
        self.horizontalLayout = QHBoxLayout(RunDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.loopCheckBox = QCheckBox(RunDialog)
        self.loopCheckBox.setObjectName(u"loopCheckBox")

        self.horizontalLayout_1.addWidget(self.loopCheckBox)


        self.verticalLayout.addLayout(self.horizontalLayout_1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.graphicsView = QGraphicsView(RunDialog)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout_2.addWidget(self.graphicsView)

        self.plainTextEdit = QPlainTextEdit(RunDialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.horizontalLayout_2.addWidget(self.plainTextEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.runButton = QPushButton(RunDialog)
        self.runButton.setObjectName(u"runButton")

        self.horizontalLayout_3.addWidget(self.runButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(RunDialog)

        QMetaObject.connectSlotsByName(RunDialog)
    # setupUi

    def retranslateUi(self, RunDialog):
        RunDialog.setWindowTitle(QCoreApplication.translate("RunDialog", u"Dialog", None))
        self.loopCheckBox.setText(QCoreApplication.translate("RunDialog", u"\u5faa\u73af\u6267\u884c", None))
        self.runButton.setText(QCoreApplication.translate("RunDialog", u"\u5f00\u59cb", None))
    # retranslateUi

