from PySide6 import QtWidgets, QtGui, QtCore
from typing import TYPE_CHECKING


class ScreenListWidgetItem(QtWidgets.QListWidgetItem):
    if TYPE_CHECKING:
        from ScreenTree import ScreenTreeWidgetItemScene
        from ScreenGraphics import ScreenGraphicsView

    def __init__(self, image: QtGui.QImage):
        super(ScreenListWidgetItem, self).__init__()
        self._treeItem = None
        self._graphicsView = None
        self.setImage(image)

    def setGraphicsView(self, graphicsView: 'ScreenGraphicsView'):
        self._graphicsView = graphicsView

    def graphicsView(self) -> 'ScreenGraphicsView':
        return self._graphicsView

    def setTreeItem(self, treeItem: 'ScreenTreeWidgetItemScene'):
        self._treeItem = treeItem

    def treeItem(self) -> 'ScreenTreeWidgetItemScene':
        return self._treeItem

    def setImage(self, image: QtGui.QImage):
        if image.height() > image.width():
            image = image.scaledToHeight(80)
        else:
            image = image.scaledToHeight(80)
        self.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(image)))
        self.setSizeHint(QtCore.QSize(image.width(), image.height()))


class ScreenListWidget(QtWidgets.QListWidget):
    def __init__(self, parent):
        super(ScreenListWidget, self).__init__(parent)
        self.setSpacing(5)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)  # 去掉边框
