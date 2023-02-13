import time

from PySide6 import QtWidgets, QtGui, QtCore

import utils
from Name import Name
from typing import TYPE_CHECKING


class ScreenGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent):
        super(ScreenGraphicsScene, self).__init__(parent)


class ScreenGraphicsItemText(QtWidgets.QGraphicsTextItem):
    def __init__(self, text, size: int = 12):
        super(ScreenGraphicsItemText, self).__init__()

        self._font = QtGui.QFont()
        self._font.setPointSize(size)
        self._font.setBold(True)

        self.setPlainText(text)
        self.setDefaultTextColor(QtGui.QColorConstants.White)
        self.setFont(self._font)


class ScreenGraphicsItemPoint(QtWidgets.QGraphicsEllipseItem):
    if TYPE_CHECKING:
        from ScreenTree import ScreenTreeWidgetItemElement

    _normalBrush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 180))
    _activeBrush = QtGui.QBrush(QtGui.QColor(0, 255, 0, 180))
    _lightBrush = QtGui.QBrush(QtGui.QColor(255, 255, 0, 180))

    def __init__(self, name: Name, rect: QtCore.QRectF):
        super(ScreenGraphicsItemPoint, self).__init__(rect)

        self._mousePressedInfo = None
        self._treeItem = None
        self.setBrush(self._normalBrush)
        self.setPen(QtCore.Qt.PenStyle.NoPen)

        topLeft = rect.normalized().topLeft()
        self._textItem = ScreenGraphicsItemText(name.id())
        self._textItem.setParentItem(self)
        self._textItem.setPos(
            topLeft.x() + ((self.boundingRect().width() - self._textItem.boundingRect().width()) / 2),
            topLeft.y() + ((self.boundingRect().height() - self._textItem.boundingRect().height()) / 2)
        )

        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setToolTip(name)

    def setTreeItem(self, treeItem: 'ScreenTreeWidgetItemElement'):
        self._treeItem = treeItem

    def treeItem(self) -> 'ScreenTreeWidgetItemElement':
        return self._treeItem

    def active(self, active=True):
        if active:
            self.setBrush(self._activeBrush)
        else:
            self.setBrush(self._normalBrush)

    def light(self):
        scene = self.scene()
        for i in range(3):
            self.setBrush(self._lightBrush)
            scene.update(self.rect())
            time.sleep(0.05)
            self.setBrush(self._normalBrush)
            scene.update(self.rect())
            time.sleep(0.05)

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem, widget: QtWidgets.QWidget) -> None:
        if self.isSelected():
            option.state = QtWidgets.QStyle.StateFlag.State_None  # 取消[选中状态]时的边框虚线
        super(ScreenGraphicsItemPoint, self).paint(painter, option, widget)

    def hoverMoveEvent(self, e: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            self.setCursor(QtCore.Qt.CursorShape.SizeAllCursor)
        else:
            self.setCursor(QtCore.Qt.CursorShape.CrossCursor)

    def mousePressEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super(ScreenGraphicsItemPoint, self).mousePressEvent(e)
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and e.button() == QtCore.Qt.MouseButton.LeftButton:
            self._mousePressedInfo = (self.scenePos(), e.scenePos(), self.mapRectToScene(self.rect()))
            self.active(active=True)

    def mouseMoveEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super(ScreenGraphicsItemPoint, self).mouseMoveEvent(e)
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and e.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self._mousePressedInfo is not None:
                self.setPos(self._mousePressedInfo[0] + (e.scenePos() - self._mousePressedInfo[1]))
        elif self._mousePressedInfo is not None:
            self._mousePressedInfo = None
            self.active(active=False)

    def mouseReleaseEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super(ScreenGraphicsItemPoint, self).mouseReleaseEvent(e)
        if self._mousePressedInfo is not None:
            self._mousePressedInfo = None
            self.active(active=False)


class ScreenGraphicsItemRect(QtWidgets.QGraphicsRectItem):
    if TYPE_CHECKING:
        from ScreenTree import ScreenTreeWidgetItemElement

    _normalBrush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 180))
    _activeBrush = QtGui.QBrush(QtGui.QColor(0, 255, 0, 180))
    _lightBrush = QtGui.QBrush(QtGui.QColor(255, 255, 0, 180))

    def __init__(self, name: Name, rect: QtCore.QRectF):
        super(ScreenGraphicsItemRect, self).__init__(rect)

        self._mousePressedInfo = None
        self._treeItem = None
        self._dragDirect = None
        self.setBrush(self._normalBrush)
        self.setPen(QtCore.Qt.PenStyle.NoPen)

        self._textItem = ScreenGraphicsItemText(name.id())
        self._textItem.setParentItem(self)
        self._textItem.setPos(rect.normalized().topLeft())
        self._textItem.setAcceptHoverEvents(True)

        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setToolTip(name)
        # TODO 解决鼠标在子item上时无法触发父item的鼠标事件
        # self.installSceneEventFilter(self._textItem)
        # self.setFiltersChildEvents(True)

    def setTreeItem(self, treeItem: 'ScreenTreeWidgetItemElement'):
        self._treeItem = treeItem

    def treeItem(self) -> 'ScreenTreeWidgetItemElement':
        return self._treeItem

    def active(self, active=True):
        if active:
            self.setBrush(self._activeBrush)
        else:
            self.setBrush(self._normalBrush)

    def light(self):
        scene = self.scene()
        for i in range(3):
            self.setBrush(self._lightBrush)
            scene.update(self.rect())
            time.sleep(0.05)
            self.setBrush(self._normalBrush)
            scene.update(self.rect())
            time.sleep(0.05)

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionGraphicsItem,
              widget: QtWidgets.QWidget) -> None:
        if self.isSelected():
            option.state = QtWidgets.QStyle.StateFlag.State_None  # 取消[选中状态]时的边框虚线
        super(ScreenGraphicsItemRect, self).paint(painter, option, widget)

    def hoverMoveEvent(self, e: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self._dragDirect = None
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier:
            direct = utils.pointInRectDirect(QtCore.QPointF(e.scenePos()), self.mapRectToScene(self.rect()), 20)
            cursor = utils.directToCursorSizeStyle(direct)
            if cursor is not None:
                self.setCursor(cursor)
                self._dragDirect = direct
            else:
                self.setCursor(QtCore.Qt.CursorShape.SizeAllCursor)
        else:
            self.setCursor(QtCore.Qt.CursorShape.CrossCursor)

    def mousePressEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super(ScreenGraphicsItemRect, self).mousePressEvent(e)
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and e.button() == QtCore.Qt.MouseButton.LeftButton:
            self._mousePressedInfo = (self.scenePos(), e.scenePos(), self.mapRectToScene(self.rect()))
            self.active(active=True)

    def mouseMoveEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super(ScreenGraphicsItemRect, self).mouseMoveEvent(e)
        if e.modifiers() == QtCore.Qt.KeyboardModifier.ControlModifier and e.buttons() == QtCore.Qt.MouseButton.LeftButton:
            if self._mousePressedInfo is not None:
                if self._dragDirect is not None:
                    self.dragSize(self._dragDirect, self._mousePressedInfo[2],
                                  self._mousePressedInfo[1], e.scenePos())
                else:
                    self.setPos(self._mousePressedInfo[0] + (e.scenePos() - self._mousePressedInfo[1]))
        elif self._mousePressedInfo is not None:
            self._mousePressedInfo = None
            self.active(active=False)

    def mouseReleaseEvent(self, e: QtWidgets.QGraphicsSceneMouseEvent) -> None:
        super(ScreenGraphicsItemRect, self).mouseReleaseEvent(e)
        if self._mousePressedInfo is not None:
            self._mousePressedInfo = None
            self.active(active=False)

    def dragSize(self, direct, mousePressedSceneRect, mousePressedScenePos, mouseMoveScenePos):
        scenePos = mouseMoveScenePos - mousePressedScenePos
        sceneRect = QtCore.QRectF(mousePressedSceneRect)  # 复制出来防止原数据被修改
        if direct & utils.DIRECT_LEFT != 0:
            sceneRect.setX(sceneRect.x() + scenePos.x())
        elif direct & utils.DIRECT_RIGHT != 0:
            sceneRect.setWidth(sceneRect.width() + scenePos.x())

        if direct & utils.DIRECT_TOP != 0:
            sceneRect.setY(sceneRect.y() + scenePos.y())
        elif direct & utils.DIRECT_BOTTOM != 0:
            sceneRect.setHeight(sceneRect.height() + scenePos.y())

        self.setRect(self.mapRectFromScene(sceneRect))

    def setRect(self, rect: QtCore.QRectF) -> None:
        super(ScreenGraphicsItemRect, self).setRect(rect)
        textRect = rect.normalized()
        self._textItem.setPos(self.mapFromScene(
            QtCore.QPointF(textRect.topLeft())
        ))


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
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.NoBrush)
        self.setBackgroundBrush(brush)
        self.setStyleSheet("border:0px; padding:0px;")
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

    def loadScene(self, image: QtGui.QImage):
        self._sceneImage = image
        if self._sceneItem is None:
            self._sceneItem = self.scene().addPixmap(QtGui.QPixmap.fromImage(image))
        else:
            self._sceneItem.setPixmap(QtGui.QPixmap.fromImage(image))
        self.scene().setSceneRect(0, 0, image.width(), image.height())
        self.fitSize()

    def image(self) -> QtGui.QImage:
        return self._sceneImage

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        scale = 1.2 if e.angleDelta().y() > 0 else 1 / 1.2
        scaledRect = self.transform().scale(scale, scale).mapRect(QtCore.QRectF(0, 0, self._sceneImage.width(), self._sceneImage.height()))
        # 由于使用了固定的步长（1.2）来缩放，所以缩放比例只会出现 -2.4,-1.2,0,1.2,2.4
        # 因此滚轮正传反转一次会刚好还原，所以不需要操心：本次缩放后高度比初始小，不缩放又比初始大的情况
        if scaledRect.height() < self.height():
            return
        self.scale(scale, scale)

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        super(ScreenGraphicsView, self).paintEvent(e)

        pos = self._mouseMoveInfo
        if pos is None:
            return

        # 显示参考线
        painter = QtGui.QPainter(self.viewport())
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColorConstants.White)
        painter.setPen(pen)
        painter.drawLine(0, pos.y(), self.width(), pos.y())
        painter.drawLine(pos.x(), 0, pos.x(), self.height())

        # 显示坐标位置
        scenePos = self.mapToScene(QtCore.QPoint(pos.x(), pos.y()))
        painter.drawText(QtCore.QPointF(0, 10), "%d,%d" % (scenePos.x(), scenePos.y()))

    def fitSize(self):
        scale = self.height() / self._sceneImage.height()
        width = self._sceneImage.width() * scale
        transform = QtGui.QTransform(scale, self.transform().m12(), self.transform().m21(), scale, self.transform().dx(), self.transform().dy())
        self.setTransform(transform)
        self.sizeChanged.emit(width, self.height())

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        super(ScreenGraphicsView, self).resizeEvent(e)
        # 宽度随高度的比例调整，所以无视宽度resize
        if e.oldSize().height() == e.size().height():
            return
        self.fitSize()

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        super(ScreenGraphicsView, self).mousePressEvent(e)
        centerPos = self.mapToScene(e.position().toPoint()) - e.position() + QtCore.QPointF(self.width() / 2, self.height() / 2)
        self._drawingRectItem = None
        self._mousePressedInfo = (e.position(), e.button(), centerPos)

    def mouseMoveEvent(self, e: QtGui.QMouseEvent) -> None:
        super(ScreenGraphicsView, self).mouseMoveEvent(e)

        self._mouseMoveInfo = (e.position())
        self.viewport().update()  # trigger paintEvent

        if e.modifiers() == QtCore.Qt.KeyboardModifier.NoModifier and self._mousePressedInfo is not None:
            pos, button, centerPos = self._mousePressedInfo
            if e.buttons() == QtCore.Qt.MouseButton.LeftButton:  # 绘图
                if self._drawingRectItem is None:
                    self._drawingRectItem = self.addRectItem(pos, e.position())
                else:
                    self.updateCurrentDrawingRectItem(pos, e.position())
            elif e.buttons() == QtCore.Qt.MouseButton.RightButton:  # 拖放
                self.centerOn(centerPos - (self.mapToScene(e.position().toPoint()) - self.mapToScene(pos.toPoint())))
        else:
            self._drawingRectItem = None

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        super(ScreenGraphicsView, self).mouseReleaseEvent(e)
        if e.button() == QtCore.Qt.MouseButton.LeftButton and self._mousePressedInfo is not None:
            pos = self._mousePressedInfo[0]
            if e.modifiers() == QtCore.Qt.KeyboardModifier.NoModifier:
                if self._drawingRectItem is None:  # 鼠标按下后没有移动
                    self.addPointItem(e.position())
            elif e.modifiers() == QtCore.Qt.KeyboardModifier.AltModifier:
                if e.position().x() == pos.x() and e.position().y() == pos.y():
                    self.clickRequested.emit(self.mapToScene(e.position().toPoint()).toPoint())
                else:
                    self.moveRequested.emit(self.mapToScene(pos.toPoint()).toPoint(), self.mapToScene(e.position().toPoint()).toPoint())

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

    def updateCurrentDrawingRectItem(self, mousePressedPos: QtCore.QPointF, mouseMovePos: QtCore.QPointF):
        point1 = self.mapToScene(mousePressedPos.toPoint())
        point2 = self.mapToScene(mouseMovePos.toPoint())
        rect = QtCore.QRectF(point1, point2)
        self._drawingRectItem.setRect(rect)

    def addRectItem(self, mousePressedPos: QtCore.QPointF, mouseMovePos: QtCore.QPointF):
        name = Name("", id=f"r{self._counter.next()}")
        topLeft = self.mapToScene(mousePressedPos.toPoint())
        bottomRight = self.mapToScene(mouseMovePos.toPoint())
        item = self.createRectItem(name, QtCore.QRectF(topLeft, bottomRight))
        self.addedElement.emit(self, name, item)
        return item

    def addPointItem(self, mousePressedPos: QtCore.QPointF):
        name = Name("", id=f"p{self._counter.next()}")
        width = self.transform().m11() * self._sceneImage.width() * 0.02  # 通过缩放比例显示点的大小
        height = self.transform().m22() * self._sceneImage.width() * 0.02  # 通过缩放比例显示点的大小
        topLeft = self.mapToScene(QtCore.QPoint(mousePressedPos.x() - width, mousePressedPos.y() - height))
        bottomRight = self.mapToScene(QtCore.QPoint(mousePressedPos.x() + width, mousePressedPos.y() + height))
        item = self.createPointItem(name, QtCore.QRectF(topLeft, bottomRight))
        self.addedElement.emit(self, name, item)
        return item

    def createRectItem(self, name: Name, rect: QtCore.QRectF):
        item = ScreenGraphicsItemRect(name, rect)
        self.scene().addItem(item)
        return item

    def createPointItem(self, name: Name, rect: QtCore.QRectF):
        item = ScreenGraphicsItemPoint(name, rect)
        self.scene().addItem(item)
        return item
