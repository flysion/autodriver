from PySide6 import QtWidgets, QtGui, QtCore

from EditorTabView import EditorTabView


class EditorTabBar(QtWidgets.QTabBar):
    def __init__(self, parent):
        super(EditorTabBar, self).__init__(parent)

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        super(EditorTabBar, self).paintEvent(e)

        # 小红点，提示文件有修改
        # painter = QtGui.QPainter(self)
        # painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0, 180)))
        # painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 180)))
        # for i in range(self.count()):
        #     rect = self.tabRect(i)
        #     point = rect.topRight() + QtCore.QPoint(-5, 5)
        #     painter.drawEllipse(point, 2, 2)


class EditorTabWidget(QtWidgets.QTabWidget):
    gotoTreeWidgetAction = QtCore.Signal(EditorTabView)

    def __init__(self, parent):
        super(EditorTabWidget, self).__init__(parent)
        self.setTabsClosable(False)
        self.setTabBar(EditorTabBar(self))
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    def on_customContextMenuRequested(self, pos: QtCore.QPoint):
        index = self.tabBar().tabAt(pos)
        menu = QtWidgets.QMenu()

        if index >= 0:
            closeAction = QtGui.QAction("关闭", menu)
            closeAction.triggered.connect(lambda checked=False: self.closeTab(index))
            menu.addAction(closeAction)
            menu.addSeparator()

            gotoTreeWidgetAction = QtGui.QAction("定位到列表", menu)
            gotoTreeWidgetAction.triggered.connect(lambda checked=False: self.gotoTreeWidgetAction.emit(self.widget(index)))
            menu.addAction(gotoTreeWidgetAction)
            menu.addSeparator()

            if self.count() > 1:
                closeOtherAction = QtGui.QAction("关闭其他", menu)
                closeOtherAction.triggered.connect(lambda checked=False: self.closeOther(index))
                menu.addAction(closeOtherAction)

            if index > 0:
                closeLeftAction = QtGui.QAction("关闭左边", menu)
                closeLeftAction.triggered.connect(lambda checked=False: self.closeLeft(index))
                menu.addAction(closeLeftAction)

            if index < self.count() - 1:
                closeRightAction = QtGui.QAction("关闭右边", menu)
                closeRightAction.triggered.connect(lambda checked=False: self.closeRight(index))
                menu.addAction(closeRightAction)

        if self.count() > 1:
            closeAllAction = QtGui.QAction("关闭全部", menu)
            closeAllAction.triggered.connect(lambda checked=False: self.clear())
            menu.addAction(closeAllAction)

        menu.exec(QtGui.QCursor.pos())

    def closeTab(self, index: int):
        self.removeTab(index)

    def closeOther(self, index: int):
        self.closeLeft(index)
        self.closeRight(0)

    def closeLeft(self, index: int):
        for i in range(0, index):
            self.closeTab(0)

    def closeRight(self, index: int):
        for i in range(index + 1, self.count()):
            self.closeTab(index + 1)

    def removeTabByWidget(self, widget):
        index = self.indexOf(widget)
        if index != -1:
            self.removeTab(index)
