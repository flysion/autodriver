import time
from typing import TYPE_CHECKING

from PySide6 import QtWidgets, QtGui, QtCore

import utils
from Name import Name

_normalBrush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 180))
_activeBrush = QtGui.QBrush(QtGui.QColor(0, 255, 0, 180))
_lightBrush = QtGui.QBrush(QtGui.QColor(255, 255, 0, 180))

_backgroundPen = QtGui.QPen()
_backgroundPen.setColor(QtGui.QColor(200, 200, 200))
_backgroundPen.setWidth(1)

_backgroundBrush = QtGui.QBrush(QtGui.QColor(100, 100, 100))

_textPen = QtGui.QPen()
_textPen.setWidth(1)
_textPen.setColor(QtGui.QColor(255, 255, 255))

_textFont = QtGui.QFont()
_textFont.setPointSize(18)

_posTextPen = QtGui.QPen()
_posTextPen.setWidth(2)
_posTextPen.setColor(QtGui.QColorConstants.Red)


class ScreenGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent):
        super(ScreenGraphicsScene, self).__init__(parent)


class ScreenGraphicsItemPoint(QtWidgets.QGraphicsEllipseItem):
    if TYPE_CHECKING:
        from ScreenTree import ScreenTreeWidgetItemElement

    def __init__(self, name: Name, point: QtCore.QPointF):
        super(ScreenGraphicsItemPoint, self).__init__()

        self._name = name
        self._mousePressedInfo = None
        self._active = False
        self._treeItem = None
        self.setBrush(_normalBrush)
        self.setPen(QtCore.Qt.PenStyle.NoPen)

        rect = QtCore.QRectF(QtCore.QPointF(point.x() - 20, point.y() - 20),
                             QtCore.QPointF(point.x() + 20, point.y() + 20))

        self.setRect(rect)
        self.setAcceptHoverEvents(True)
        # self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setToolTip(name)

    def setTreeItem(self, treeItem: 'ScreenTreeWidgetItemElement'):
        self._treeItem = treeItem

    def treeItem(self) -> 'ScreenTreeWidgetItemElement':
        return self._treeItem

    def setActive(self, active):
        self._active = active
        if active:
            self.setBrush(_activeBrush)
        else:
            self.setBrush(_normalBrush)

    def active(self):
        return self._active

    def light(self):
        scene = self.scene()
        for i in range(3):
            self.setBrush(_lightBrush)
            scene.update(self.rect())
            time.sleep(0.05)
            self.setBrush(_normalBrush)
            scene.update(self.rect())
            time.sleep(0.05)

    def sceneEvent(self, e):
        if isinstance(e, QtWidgets.QGraphicsSceneMouseEvent):
            if e.type() == QtCore.QEvent.Type.GraphicsSceneMousePress:
                self.mousePressEvent(e)
            elif e.type() == QtCore.QEvent.Type.GraphicsSceneMouseMove:
                self.mouseMoveEvent(e)
            elif e.type() == QtCore.QEvent.Type.GraphicsSceneMouseRelease:
                self.mouseReleaseEvent(e)
            else:
                return False
        elif isinstance(e, QtWidgets.QGraphicsSceneHoverEvent):
            self.hoverMoveEvent(e)
        else:
            return False
        return True

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget) -> None:
        super(ScreenGraphicsItemPoint, self).paint(painter, option, widget)
        painter.save()
        painter.setPen(_textPen)
        painter.setFont(_textFont)
        painter.drawText(self.rect(), QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignHCenter, self._name.id())
        painter.restore()

    def hoverMoveEvent(self, e: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            self.setCursor(QtCore.Qt.CursorShape.SizeAllCursor)
        else:
            self.setCursor(QtCore.Qt.CursorShape.CrossCursor)

    def mousePressEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and e.button() == QtCore.Qt.MouseButton.LeftButton:
            self._mousePressedInfo = (self.rect(), e.scenePos(), self.mapRectToScene(self.rect()))
            self.setActive(True)
            return
        self._mousePressedInfo = None
        self.setActive(False)

    def mouseMoveEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and e.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self._mousePressedInfo is not None:
                sceneBottomRight = self.scene().sceneRect().bottomRight()
                rect = self._mousePressedInfo[0].translated(e.scenePos() - self._mousePressedInfo[1])
                topLeft = rect.topLeft()
                rect.moveTopLeft(QtCore.QPointF(min(max(0, topLeft.x()), sceneBottomRight.x() - rect.width()),
                                                min(max(0, topLeft.y()), sceneBottomRight.y() - rect.height())))
                self.setRect(rect)
                return
        self._mousePressedInfo = None
        self.setActive(False)

    def mouseReleaseEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self._mousePressedInfo is not None:
            self._mousePressedInfo = None
            self.setActive(False)


class ScreenGraphicsItemRect(QtWidgets.QGraphicsRectItem):
    if TYPE_CHECKING:
        from ScreenTree import ScreenTreeWidgetItemElement

    def __init__(self, name: Name, rect: QtCore.QRectF):
        super(ScreenGraphicsItemRect, self).__init__(rect)

        self._name = name
        self._active = False
        self._mousePressedInfo = None
        self._treeItem = None
        self._dragInfo = None

        self.setAcceptHoverEvents(True)
        # self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setToolTip(name)
        self.setBrush(_normalBrush)
        self.setPen(QtCore.Qt.PenStyle.NoPen)

    def setTreeItem(self, treeItem: 'ScreenTreeWidgetItemElement'):
        self._treeItem = treeItem

    def treeItem(self) -> 'ScreenTreeWidgetItemElement':
        return self._treeItem

    def setActive(self, active):
        self._active = active
        if active:
            self.setBrush(_activeBrush)
        else:
            self.setBrush(_normalBrush)

    def active(self):
        return self._active

    def light(self):
        scene = self.scene()
        for i in range(3):
            self.setBrush(_lightBrush)
            scene.update(self.rect())
            time.sleep(0.05)
            self.setBrush(_normalBrush)
            scene.update(self.rect())
            time.sleep(0.05)

    def sceneEvent(self, e):
        if isinstance(e, QtWidgets.QGraphicsSceneMouseEvent):
            if e.type() == QtCore.QEvent.Type.GraphicsSceneMousePress:
                self.mousePressEvent(e)
            elif e.type() == QtCore.QEvent.Type.GraphicsSceneMouseMove:
                self.mouseMoveEvent(e)
            elif e.type() == QtCore.QEvent.Type.GraphicsSceneMouseRelease:
                self.mouseReleaseEvent(e)
            else:
                return False
        elif isinstance(e, QtWidgets.QGraphicsSceneHoverEvent):
            self.hoverMoveEvent(e)
        else:
            return False
        return True

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget) -> None:
        super(ScreenGraphicsItemRect, self).paint(painter, option, widget)
        painter.save()
        painter.setPen(_textPen)
        painter.setFont(_textFont)
        painter.drawText(self.rect().adjusted(10, 10, 0, 0), self._name.id())
        painter.restore()

    def hoverMoveEvent(self, e: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self._dragInfo = None
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            direct = utils.pointInRectDirect(QtCore.QPointF(e.scenePos()), self.mapRectToScene(self.rect()), 20)
            cursor = utils.directToCursorSizeStyle(direct)
            if cursor is not None:
                self.setCursor(cursor)
                self._dragInfo = (direct,)
            else:
                self.setCursor(QtCore.Qt.CursorShape.SizeAllCursor)
        else:
            self.setCursor(QtCore.Qt.CursorShape.CrossCursor)

    def mousePressEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and e.button() == QtCore.Qt.MouseButton.LeftButton:
            self._mousePressedInfo = (self.rect(), self.mapRectToScene(self.rect()), e.scenePos())
            self.setActive(True)
            return
        self._mousePressedInfo = None
        self.setActive(False)

    def mouseMoveEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and e.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self._mousePressedInfo is not None:
                pressItemRect, pressItemSceneRect, pressPos = self._mousePressedInfo
                if self._dragInfo is not None:
                    self.dragSize(self._dragInfo[0], pressItemSceneRect, pressPos, e.scenePos())
                else:
                    sceneBottomRight = self.scene().sceneRect().bottomRight()
                    rect = pressItemRect.translated(e.scenePos() - pressPos)
                    topLeft = rect.topLeft()
                    rect.moveTopLeft(QtCore.QPointF(min(max(0, topLeft.x()), sceneBottomRight.x() - rect.width()),
                                                    min(max(0, topLeft.y()), sceneBottomRight.y() - rect.height())))
                    self.setRect(rect)
                return
        self._mousePressedInfo = None
        self.setActive(False)

    def mouseReleaseEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self._mousePressedInfo is not None:
            self._mousePressedInfo = None
            self.setActive(False)

    def dragSize(self, direct, pressItemSceneRect, pressPos, movePos):
        scenePos = movePos - pressPos
        rect = QtCore.QRectF(pressItemSceneRect)
        if direct & utils.DIRECT_LEFT != 0:
            rect.setX(rect.x() + scenePos.x())
        elif direct & utils.DIRECT_RIGHT != 0:
            rect.setWidth(rect.width() + scenePos.x())

        if direct & utils.DIRECT_TOP != 0:
            rect.setY(rect.y() + scenePos.y())
        elif direct & utils.DIRECT_BOTTOM != 0:
            rect.setHeight(rect.height() + scenePos.y())

        self.setRect(self.scene().sceneRect().intersected(self.mapRectFromScene(rect).normalized()))


class ScreenGraphicsView(QtWidgets.QGraphicsView):
    if TYPE_CHECKING:
        from ScreenList import ScreenListWidgetItem
        from ScreenTree import ScreenTreeWidgetItemScene

    sizeChanged = QtCore.Signal(int, int)
    addedElement = QtCore.Signal(object, tuple, QtWidgets.QGraphicsItem)
    clickRequested = QtCore.Signal(QtCore.QPoint)
    moveRequested = QtCore.Signal(QtCore.QPoint, QtCore.QPoint)

    def __init__(self, counter: 'Counter.Counter', *args, **kwargs):
        super(ScreenGraphicsView, self).__init__(*args, **kwargs)

        self.setAutoFillBackground(False)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("border:0px; background:transparent")
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)  # 消除拖动残影
        self.setTransformationAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setScene(ScreenGraphicsScene(self))
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.NoDrag)  # 没有拖拽框
        self.setMouseTracking(True)  # 让控件没有获取焦点的情况下也能触发鼠标事件
        self.installEventFilter(self)  # 使可触发 filterEvent，用于处理鼠标进入和离开事件
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.CrossCursor))

        self._counter = counter
        self._sceneImage: QtGui.QImage = None
        self._sceneItem: QtWidgets.QGraphicsPixmapItem = None
        self._mousePressedInfo = None
        self._mouseMoveInfo = None
        self._drawingRectItem = None
        self._listItem = None
        self._treeItem = None

    def setListItem(self, listItem: 'ScreenListWidgetItem'):
        self._listItem = listItem

    def listItem(self) -> 'ScreenListWidgetItem':
        return self._listItem

    def setTreeItem(self, treeItem: 'ScreenTreeWidgetItemScene'):
        self._treeItem = treeItem

    def treeItem(self) -> 'ScreenTreeWidgetItemScene':
        return self._treeItem

    def setSceneImage(self, image: QtGui.QImage):
        self._sceneImage = image
        if self._sceneItem is None:
            self._sceneItem = self.scene().addPixmap(QtGui.QPixmap.fromImage(image))
        else:
            self._sceneItem.setPixmap(QtGui.QPixmap.fromImage(image))
        self.scene().setSceneRect(0, 0, self._sceneImage.width(), self._sceneImage.height())
        self.adjustSize()
        self.adjustSceneSize()

    def sceneImage(self) -> QtGui.QImage:
        return self._sceneImage

    def sceneItem(self) -> QtWidgets.QGraphicsPixmapItem:
        return self._sceneItem

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        scale = 1.2 if e.angleDelta().y() > 0 else 1 / 1.2
        self.scale(scale, scale)

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        painter.save()

        painter.setBrush(_backgroundBrush)
        painter.setPen(_backgroundPen)

        painter.drawRect(rect)

        topLeft = rect.topLeft().toPoint()
        bottomRight = rect.bottomRight().toPoint()
        for x in range(topLeft.x() + 20, bottomRight.x(), 20):
            painter.drawLine(QtCore.QPoint(x, topLeft.y()), QtCore.QPoint(x, bottomRight.y()))
        for y in range(topLeft.y() + 20, bottomRight.y(), 20):
            painter.drawLine(QtCore.QPoint(topLeft.x(), y), QtCore.QPoint(bottomRight.x(), y))

        painter.restore()

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        super(ScreenGraphicsView, self).paintEvent(e)

        if self._mouseMoveInfo is None:
            return

        pos, scenePos = self._mouseMoveInfo
        if not self.sceneRect().contains(scenePos):
            return

        # 显示参考线
        painter = QtGui.QPainter(self.viewport())
        painter.setPen(_posTextPen)
        painter.drawLine(0, pos.y(), self.width(), pos.y())
        painter.drawLine(pos.x(), 0, pos.x(), self.height())
        # 显示坐标位置
        pointColor = self._sceneImage.pixelColor(scenePos.toPoint())
        text = "%d,%d,#%s" % (scenePos.x(), scenePos.y(), utils.qcolor2hex(pointColor))
        painter.drawText(QtCore.QPoint(0, 10), text)

    def adjustSceneSize(self) -> None:
        if self.width() / self.height() < self._sceneImage.width() / self._sceneImage.height():
            scale = self.width() / self._sceneImage.width()
        else:
            scale = self.height() / self._sceneImage.height()
        transform = QtGui.QTransform(scale, self.transform().m12(), self.transform().m21(),
                                     scale, self.transform().dx(), self.transform().dy())
        self.setTransform(transform)

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        super(ScreenGraphicsView, self).resizeEvent(e)
        self.adjustSceneSize()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        super(ScreenGraphicsView, self).mousePressEvent(e)

        pressPos = e.position()
        pressScenePos = self.mapToScene(pressPos.toPoint())
        if self.sceneRect().contains(pressScenePos):
            pressCenterPos = pressScenePos - pressPos + QtCore.QPointF(self.width() / 2, self.height() / 2)
            self._drawingRectItem = None
            self._mousePressedInfo = (pressPos, e.button(), pressCenterPos, pressScenePos)
            return
        self._drawingRectItem = None
        self._mousePressedInfo = None

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        super(ScreenGraphicsView, self).mouseMoveEvent(e)

        movePos = e.position()
        moveScenePos = self.mapToScene(movePos.toPoint())
        self._mouseMoveInfo = (movePos, moveScenePos)
        self.viewport().update()  # trigger paintEvent

        if e.modifiers() == QtCore.Qt.KeyboardModifier.NoModifier and self._mousePressedInfo is not None:
            pressPos, pressButton, pressCenterPos, pressScenePos = self._mousePressedInfo
            if e.buttons() == QtCore.Qt.MouseButton.LeftButton:  # 绘图
                if self._drawingRectItem is None:
                    self._drawingRectItem = self.addRectItem(pressScenePos, moveScenePos)
                else:
                    self.updateCurrentDrawingRectItem(pressScenePos, moveScenePos)
                return
            elif e.buttons() == QtCore.Qt.MouseButton.RightButton:  # 拖放
                self.centerOn(pressCenterPos - (moveScenePos - pressScenePos))
                return
        self._drawingRectItem = None
        self._mousePressedInfo = None

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        super(ScreenGraphicsView, self).mouseReleaseEvent(e)

        releasePos = e.position()
        releaseScenePos = self.mapToScene(releasePos.toPoint())

        if e.button() == QtCore.Qt.MouseButton.LeftButton and self._mousePressedInfo is not None:
            pressPos, _, _, pressScenePos = self._mousePressedInfo
            if e.modifiers() == QtCore.Qt.KeyboardModifier.NoModifier:
                if self._drawingRectItem is None:  # 鼠标按下后没有移动
                    self.addPointItem(releaseScenePos)
            elif e.modifiers() == QtCore.Qt.KeyboardModifier.AltModifier:
                if releasePos.x() == pressPos.x() and releasePos.y() == pressPos.y():
                    self.clickRequested.emit(releaseScenePos.toPoint())
                else:
                    self.moveRequested.emit(pressScenePos.toPoint(), releaseScenePos.toPoint())

        self._drawingRectItem = None
        self._mousePressedInfo = None

    def eventFilter(self, o: QtCore.QObject, e: QtCore.QEvent) -> bool:
        if o == self:
            if e.type() == QtCore.QEvent.Type.Enter:
                pass
            elif e.type() == QtCore.QEvent.Type.Leave:
                self._mouseMoveInfo = None
                self.viewport().update()  # trigger paintEvent
        return super(ScreenGraphicsView, self).eventFilter(o, e)

    def updateCurrentDrawingRectItem(self, topLeft: QtCore.QPointF, bottomRight: QtCore.QPointF):
        rect = self.sceneRect().intersected(QtCore.QRectF(topLeft, bottomRight).normalized())
        self._drawingRectItem.setRect(rect)

    def addRectItem(self, topLeft: QtCore.QPointF, bottomRight: QtCore.QPointF):
        name = Name("", id=f"r{self._counter.next()}")
        rect = self.sceneRect().intersected(QtCore.QRectF(topLeft, bottomRight).normalized())
        item = self.createRectItem(name, rect)
        self.addedElement.emit(self, name, item)
        return item

    def addPointItem(self, point: QtCore.QPointF):
        name = Name("", id=f"p{self._counter.next()}")
        item = self.createPointItem(name, point)
        self.addedElement.emit(self, name, item)
        return item

    def createRectItem(self, name: Name, rect: QtCore.QRectF):
        item = ScreenGraphicsItemRect(name, rect)
        self.scene().addItem(item)
        return item

    def createPointItem(self, name: Name, point: QtCore.QPointF):
        item = ScreenGraphicsItemPoint(name, point)
        self.scene().addItem(item)
        return item
