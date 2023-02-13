# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLayout, QListView, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QTreeWidgetItem, QVBoxLayout, QWidget)

from EditorTab import EditorTabWidget
from EditorTree import EditorTreeWidget
from ScreenList import ScreenListWidget
from ScreenTab import ScreenTabWidget
from ScreenTree import ScreenTreeWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(779, 497)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.openMenu = QAction(MainWindow)
        self.openMenu.setObjectName(u"openMenu")
        self.saveMenu = QAction(MainWindow)
        self.saveMenu.setObjectName(u"saveMenu")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.widget_1 = QWidget(self.centralwidget)
        self.widget_1.setObjectName(u"widget_1")
        self.horizontalLayout_1 = QHBoxLayout(self.widget_1)
        self.horizontalLayout_1.setSpacing(0)
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_1")
        self.horizontalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_1 = QGridLayout()
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.gridLayout_1.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_1.setHorizontalSpacing(0)
        self.gridLayout_1.setVerticalSpacing(5)
        self.screenListWidget = ScreenListWidget(self.widget_1)
        self.screenListWidget.setObjectName(u"screenListWidget")
        self.screenListWidget.setMinimumSize(QSize(0, 105))
        self.screenListWidget.setMaximumSize(QSize(16777215, 105))
        self.screenListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.screenListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.screenListWidget.setAutoScrollMargin(10)
        self.screenListWidget.setIconSize(QSize(80, 80))
        self.screenListWidget.setMovement(QListView.Static)
        self.screenListWidget.setFlow(QListView.TopToBottom)
        self.screenListWidget.setResizeMode(QListView.Adjust)
        self.screenListWidget.setSpacing(4)
        self.screenListWidget.setViewMode(QListView.IconMode)

        self.gridLayout_1.addWidget(self.screenListWidget, 1, 0, 1, 2)

        self.screenTabWidget = ScreenTabWidget(self.widget_1)
        self.screenTabWidget.setObjectName(u"screenTabWidget")

        self.gridLayout_1.addWidget(self.screenTabWidget, 0, 0, 1, 2)


        self.horizontalLayout_1.addLayout(self.gridLayout_1)


        self.horizontalLayout.addWidget(self.widget_1)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(250, 0))
        self.widget_2.setMaximumSize(QSize(250, 16777215))
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 0, 0, 0)
        self.screenTreeWidget = ScreenTreeWidget(self.widget_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.screenTreeWidget.setHeaderItem(__qtreewidgetitem)
        self.screenTreeWidget.setObjectName(u"screenTreeWidget")
        self.screenTreeWidget.setMinimumSize(QSize(0, 0))
        self.screenTreeWidget.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.screenTreeWidget)


        self.horizontalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(250, 0))
        self.widget_3.setMaximumSize(QSize(250, 16777215))
        self.widget_3.setAutoFillBackground(False)
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 0, 0, 0)
        self.editorTreeWidget = EditorTreeWidget(self.widget_3)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.editorTreeWidget.setHeaderItem(__qtreewidgetitem1)
        self.editorTreeWidget.setObjectName(u"editorTreeWidget")
        self.editorTreeWidget.setMinimumSize(QSize(0, 0))
        self.editorTreeWidget.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_3.addWidget(self.editorTreeWidget)


        self.horizontalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.centralwidget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, 0, 0, 0)
        self.editorTabWidget = EditorTabWidget(self.widget_4)
        self.editorTabWidget.setObjectName(u"editorTabWidget")

        self.horizontalLayout_4.addWidget(self.editorTabWidget)


        self.horizontalLayout.addWidget(self.widget_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 779, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.openMenu)
        self.menu.addAction(self.saveMenu)

        self.retranslateUi(MainWindow)

        self.screenTabWidget.setCurrentIndex(-1)
        self.editorTabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.openMenu.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00(&O)", None))
        self.saveMenu.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58(&S)", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6(&F)", None))
    # retranslateUi

