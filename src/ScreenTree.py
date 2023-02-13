from typing import Callable, TYPE_CHECKING, Union

from PySide6 import QtWidgets, QtGui, QtCore

from Name import Name


class ScreenTreeWidgetItemNameChangeEvent:
    def __init__(self, name: Name, oldName: Name, success: Callable):
        self._name = name
        self._oldName = oldName
        self._success = success

    def name(self):
        return self._name

    def oldName(self):
        return self._oldName

    def accept(self):
        self._success()


class ScreenTreeWidgetItemWidget(QtWidgets.QWidget):
    def __init__(self, name: Name):
        super(ScreenTreeWidgetItemWidget, self).__init__()

        self._name = name

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(5, 5, 5, 5)
        self._layout.setSpacing(5)
        self.setLayout(self._layout)

        if name.id() is not None:
            self._label0 = QtWidgets.QLabel()
            self._label0.setText(name.id())
            self._label0.adjustSize()
            self._label0.setMaximumWidth(self._label0.width())
            self._label0.setStyleSheet("color:red;")
            self._layout.addWidget(self._label0)

        self._label1 = QtWidgets.QLabel()
        self._label1.setText(name)
        self._layout.addWidget(self._label1)

        self._menu = QtWidgets.QMenu()

        self._editor = QtWidgets.QLineEdit()
        self._editor.returnPressed.connect(self.onEditorReturnPressed)  # 回车键提交

    def onEditorReturnPressed(self):
        name = self._name.new(self._editor.text())

        def success(name=name, self=self):
            self.setModifyMode(False)
            self._label1.setText(name)
            self._name = name

        event = ScreenTreeWidgetItemNameChangeEvent(name, self._name, success)
        self.canNameChange(event)

    def eventFilter(self, o: QtCore.QObject, e: [QtCore.QEvent, QtGui.QKeyEvent]) -> bool:
        if o == self._editor:
            if e.type() == QtCore.QEvent.Type.FocusOut:
                self.setModifyMode(False)

        return super(ScreenTreeWidgetItemWidget, self).eventFilter(o, e)

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        self.setModifyMode()

    def setModifyMode(self, modifiable=True):
        if modifiable:
            self._layout.removeWidget(self._label1)
            self._label1.hide()

            self._editor.setText(self._name)
            self._layout.insertWidget(0 if self._name.id() is None else 1, self._editor)
            self._editor.setFocus()
            self._editor.show()
            self._editor.installEventFilter(self)  # 监听焦点离开事件，更适时的开启有助于性能提升
        else:
            self._layout.removeWidget(self._editor)
            self._editor.hide()
            self._editor.removeEventFilter(self)

            self._layout.insertWidget(0 if self._name.id() is None else 1, self._label1)
            self._label1.show()

    def canNameChange(self, event: ScreenTreeWidgetItemNameChangeEvent):
        event.accept()

    def name(self) -> Name:
        return self._name


class ScreenTreeWidgetItemWidgetGroup(ScreenTreeWidgetItemWidget):
    nameChange = QtCore.Signal(ScreenTreeWidgetItemNameChangeEvent)

    def __init__(self, name: Name):
        super(ScreenTreeWidgetItemWidgetGroup, self).__init__(name)

    def canNameChange(self, event: ScreenTreeWidgetItemNameChangeEvent):
        self.nameChange.emit(event)


class ScreenTreeWidgetItemWidgetScene(ScreenTreeWidgetItemWidget):
    nameChange = QtCore.Signal(ScreenTreeWidgetItemNameChangeEvent)

    def __init__(self, name: Name):
        super(ScreenTreeWidgetItemWidgetScene, self).__init__(name)

    def canNameChange(self, event: ScreenTreeWidgetItemNameChangeEvent):
        self.nameChange.emit(event)


class ScreenTreeWidgetItemWidgetElement(ScreenTreeWidgetItemWidget):
    nameChange = QtCore.Signal(ScreenTreeWidgetItemNameChangeEvent)

    def __init__(self, name: Name):
        super(ScreenTreeWidgetItemWidgetElement, self).__init__(name)

    def canNameChange(self, event: ScreenTreeWidgetItemNameChangeEvent):
        self.nameChange.emit(event)


class ScreenTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self):
        super(ScreenTreeWidgetItem, self).__init__()


class ScreenTreeWidgetItemGroup(ScreenTreeWidgetItem):
    def __init__(self):
        super(ScreenTreeWidgetItemGroup, self).__init__()
        self.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator)  # 始终显示折叠按钮

    def widget(self) -> ScreenTreeWidgetItemWidgetGroup:
        return self.treeWidget().itemWidget(self, 0)

    def name(self) -> Name:
        return self.widget().name()

    def path(self) -> str:
        return self.name()


class ScreenTreeWidgetItemScene(ScreenTreeWidgetItem):
    if TYPE_CHECKING:
        from ScreenList import ScreenListWidgetItem
        from ScreenGraphics import ScreenGraphicsView

    def __init__(self):
        super(ScreenTreeWidgetItemScene, self).__init__()
        self.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator)  # 始终显示折叠按钮
        self._graphicsView = None
        self._listItem = None

    def setGraphicsView(self, graphicsView: 'ScreenGraphicsView'):
        self._graphicsView = graphicsView

    def graphicsView(self) -> 'ScreenGraphicsView':
        return self._graphicsView

    def setListItem(self, listItem: 'ScreenListWidgetItem'):
        self._listItem = listItem

    def listItem(self) -> 'ScreenListWidgetItem':
        return self._listItem

    def widget(self) -> ScreenTreeWidgetItemWidgetScene:
        return self.treeWidget().itemWidget(self, 0)

    def name(self) -> Name:
        return self.widget().name()

    def path(self) -> str:
        return self.parent().path() + '.' + self.name()


class ScreenTreeWidgetItemElement(ScreenTreeWidgetItem):
    if TYPE_CHECKING:
        from ScreenList import ScreenListWidgetItem
        from ScreenGraphics import ScreenGraphicsItemPoint, ScreenGraphicsItemRect

    def __init__(self):
        super(ScreenTreeWidgetItemElement, self).__init__()
        self.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ChildIndicatorPolicy.DontShowIndicator)
        self._graphicsItem = None

    def setGraphicsItem(self, graphicsItem: Union['ScreenGraphicsItemPoint', 'ScreenGraphicsItemRect']):
        self._graphicsItem = graphicsItem

    def graphicsItem(self) -> Union['ScreenGraphicsItemPoint', 'ScreenGraphicsItemRect']:
        return self._graphicsItem

    def widget(self) -> ScreenTreeWidgetItemWidgetElement:
        return self.treeWidget().itemWidget(self, 0)

    def name(self) -> Name:
        return self.widget().name()

    def path(self) -> str:
        return self.parent().path() + '.' + self.name()


class ScreenTreeWidget(QtWidgets.QTreeWidget):
    addGroupTriggered = QtCore.Signal()
    addSceneOnGroupTriggered = QtCore.Signal(ScreenTreeWidgetItemGroup)
    deleteGroupTriggered = QtCore.Signal(ScreenTreeWidgetItemGroup)
    reloadSceneImageTriggered = QtCore.Signal(ScreenTreeWidgetItemScene)
    deleteSceneTriggered = QtCore.Signal(ScreenTreeWidgetItemScene)
    deleteElementTriggered = QtCore.Signal(ScreenTreeWidgetItemElement)
    groupNameChanged = QtCore.Signal(ScreenTreeWidgetItemGroup, ScreenTreeWidgetItemNameChangeEvent)
    sceneNameChanged = QtCore.Signal(ScreenTreeWidgetItemScene, ScreenTreeWidgetItemNameChangeEvent)
    elementNameChanged = QtCore.Signal(ScreenTreeWidgetItemElement, ScreenTreeWidgetItemNameChangeEvent)

    def __init__(self, parent):
        super(ScreenTreeWidget, self).__init__(parent)
        self.setHeaderHidden(True)
        self.setColumnCount(1)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)  # 单选
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)  # 去掉边框
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    def on_customContextMenuRequested(self, pos: QtCore.QPoint):
        item = self.itemAt(pos)
        if item is None:
            menu = QtWidgets.QMenu()
            addGroupAction = QtGui.QAction("添加分组", menu)
            addGroupAction.triggered.connect(lambda checked=False: self.addGroupTriggered.emit())
            menu.addAction(addGroupAction)
            expendAllAction = QtGui.QAction("展开全部", menu)
            expendAllAction.triggered.connect(lambda checked=False: self.expandAll())
            menu.addAction(expendAllAction)
            collapseAllAction = QtGui.QAction("收起全部", menu)
            collapseAllAction.triggered.connect(lambda checked=False: self.collapseAll())
            menu.addAction(collapseAllAction)
        elif isinstance(item, ScreenTreeWidgetItemGroup):
            menu = QtWidgets.QMenu()
            addScreenAction = QtGui.QAction("添加场景", menu)
            addScreenAction.triggered.connect(lambda checked=False, item=item: self.addSceneOnGroupTriggered.emit(item))
            menu.addAction(addScreenAction)
            deleteGroupAction = QtGui.QAction("删除", menu)
            deleteGroupAction.triggered.connect(lambda checked=False, item=item: self.deleteGroupTriggered.emit(item))
            menu.addAction(deleteGroupAction)
        elif isinstance(item, ScreenTreeWidgetItemScene):
            menu = QtWidgets.QMenu()
            reloadScreenImageAction = QtGui.QAction("重新加载场景", menu)
            reloadScreenImageAction.triggered.connect(lambda checked=False, item=item: self.reloadSceneImageTriggered.emit(item))
            menu.addAction(reloadScreenImageAction)
            deleteScreenAction = QtGui.QAction("删除", menu)
            deleteScreenAction.triggered.connect(lambda checked=False, item=item: self.deleteSceneTriggered.emit(item))
            menu.addAction(deleteScreenAction)
        elif isinstance(item, ScreenTreeWidgetItemElement):
            menu = QtWidgets.QMenu()
            deleteElementAction = QtGui.QAction("删除", menu)
            deleteElementAction.triggered.connect(lambda checked=False, item=item: self.deleteElementTriggered.emit(item))
            menu.addAction(deleteElementAction)
        else:
            return
        menu.exec(QtGui.QCursor.pos())

    def addGroupItem(self, name: Name) -> ScreenTreeWidgetItemGroup:
        item = ScreenTreeWidgetItemGroup()
        self.addTopLevelItem(item)

        widget = ScreenTreeWidgetItemWidgetGroup(name)
        widget.nameChange.connect(lambda event, item=item: self.groupNameChanged.emit(item, event))
        self.setItemWidget(item, 0, widget)

        return item

    def addSceneItem(self, name: Name, screenTreeWidgetItemGroup: ScreenTreeWidgetItemGroup) -> ScreenTreeWidgetItemScene:
        item = ScreenTreeWidgetItemScene()
        screenTreeWidgetItemGroup.addChild(item)

        widget = ScreenTreeWidgetItemWidgetScene(name)
        widget.nameChange.connect(lambda event, item=item: self.sceneNameChanged.emit(item, event))
        self.setItemWidget(item, 0, widget)

        return item

    def addElementItem(self, name: Name, screenTreeWidgetItemScene: ScreenTreeWidgetItemScene) -> ScreenTreeWidgetItemElement:
        item = ScreenTreeWidgetItemElement()
        screenTreeWidgetItemScene.addChild(item)

        widget = ScreenTreeWidgetItemWidgetElement(name)
        widget.nameChange.connect(lambda event, item=item: self.elementNameChanged.emit(item, event))
        self.setItemWidget(item, 0, widget)

        return item
