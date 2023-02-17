from typing import Callable, TYPE_CHECKING, Union

from PySide6 import QtWidgets, QtGui, QtCore

from Name import Name


class EditorTreeWidgetItemNameChangeEvent:
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


class EditorTreeWidgetItemWidget(QtWidgets.QWidget):
    mouseDoubleClicked = QtCore.Signal(QtGui.QMouseEvent)

    def __init__(self, name: Name):
        super(EditorTreeWidgetItemWidget, self).__init__()

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

        event = EditorTreeWidgetItemNameChangeEvent(name, self._name, success)
        self.canNameChange(event)

    def eventFilter(self, o: QtCore.QObject, e: [QtCore.QEvent, QtGui.QKeyEvent]) -> bool:
        if o == self._editor:
            if e.type() == QtCore.QEvent.Type.FocusOut:
                self.setModifyMode(False)
        return super(EditorTreeWidgetItemWidget, self).eventFilter(o, e)

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent) -> None:
        self.mouseDoubleClicked.emit(e)

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

    def canNameChange(self, event: EditorTreeWidgetItemNameChangeEvent):
        event.accept()

    def name(self) -> Name:
        return self._name


class EditorTreeWidgetItemWidgetFolder(EditorTreeWidgetItemWidget):
    nameChange = QtCore.Signal(EditorTreeWidgetItemNameChangeEvent)

    def __init__(self, name: Name):
        super(EditorTreeWidgetItemWidgetFolder, self).__init__(name)

    def canNameChange(self, event: EditorTreeWidgetItemNameChangeEvent):
        self.nameChange.emit(event)


class EditorTreeWidgetItemWidgetFile(EditorTreeWidgetItemWidget):
    nameChange = QtCore.Signal(EditorTreeWidgetItemNameChangeEvent)

    def __init__(self, name: Name):
        super(EditorTreeWidgetItemWidgetFile, self).__init__(name)

    def canNameChange(self, event: EditorTreeWidgetItemNameChangeEvent):
        self.nameChange.emit(event)


class EditorTreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self):
        super(EditorTreeWidgetItem, self).__init__()

    def __lt__(self, other: 'EditorTreeWidgetItem'):
        widget = self.treeWidget().itemWidget(self, 0)
        widget1 = self.treeWidget().itemWidget(other, 0)
        if isinstance(self, EditorTreeWidgetItemFolder) and isinstance(other, EditorTreeWidgetItemFolder):
            return widget.name() < widget1.name()
        elif isinstance(self, EditorTreeWidgetItemFolder):
            return True
        elif isinstance(other, EditorTreeWidgetItemFolder):
            return False
        else:
            return int(widget.name().id()[1:]) < int(widget1.name().id()[1:])


class EditorTreeWidgetItemFolder(EditorTreeWidgetItem):
    def __init__(self):
        super(EditorTreeWidgetItemFolder, self).__init__()

    def widget(self) -> EditorTreeWidgetItemWidgetFolder:
        return self.treeWidget().itemWidget(self, 0)

    def name(self) -> Name:
        return self.widget().name()

    def path(self) -> str:
        parent = self.parent()
        if parent is None:
            return self.name()
        else:
            return self.parent().path() + '.' + self.name()


class EditorTreeWidgetItemFile(EditorTreeWidgetItem):
    if TYPE_CHECKING:
        from EditorTabView import EditorTabView

    def __init__(self):
        super(EditorTreeWidgetItemFile, self).__init__()
        self._tabView = None
        self._textCode = ''

    def setTabView(self, tabView: 'EditorTabView'):
        self._tabView = tabView

    def tabView(self) -> 'EditorTabView':
        return self._tabView

    def setTextCode(self, textCode: str):
        self._textCode = textCode

    def textCode(self) -> str:
        return self._textCode

    def widget(self) -> EditorTreeWidgetItemWidgetFile:
        return self.treeWidget().itemWidget(self, 0)

    def name(self) -> Name:
        return self.widget().name()

    def path(self) -> str:
        parent = self.parent()
        if parent is None:
            return self.name()
        else:
            return self.parent().path() + '.' + self.name()


class EditorTreeWidget(QtWidgets.QTreeWidget):
    addFolderTriggered = QtCore.Signal()
    addFileTriggered = QtCore.Signal()
    openFileTriggered = QtCore.Signal(QtWidgets.QTreeWidgetItem)
    runFileTriggered = QtCore.Signal(QtWidgets.QTreeWidgetItem)
    addFolderOnFolderTriggered = QtCore.Signal(QtWidgets.QTreeWidgetItem)
    addFileOnFolderTriggered = QtCore.Signal(QtWidgets.QTreeWidgetItem)
    deleteFolderTriggered = QtCore.Signal(QtWidgets.QTreeWidgetItem)
    deleteFileTriggered = QtCore.Signal(QtWidgets.QTreeWidgetItem)
    folderNameChanged = QtCore.Signal(QtWidgets.QTreeWidgetItem, EditorTreeWidgetItemNameChangeEvent)
    fileNameChanged = QtCore.Signal(QtWidgets.QTreeWidgetItem, EditorTreeWidgetItemNameChangeEvent)

    def __init__(self, parent):
        super(EditorTreeWidget, self).__init__(parent)
        self.setHeaderHidden(True)
        self.setColumnCount(1)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)  # 单选
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)  # 去掉边框
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)
        # self.setStyle(QtWidgets.QStyleFactory.create("windows"))

    def removeItem(self, item: EditorTreeWidgetItem):
        if item.parent() is None:
            self.takeTopLevelItem(self.indexOfTopLevelItem(item))
        else:
            item.parent().removeChild(item)

    def on_customContextMenuRequested(self, pos: QtCore.QPoint):
        item: Union[None, EditorTreeWidgetItemWidgetFolder, EditorTreeWidgetItemWidgetFile] = self.itemAt(pos)
        widget = self.itemWidget(item, 0)

        if item is None:
            menu = QtWidgets.QMenu()
            addFolderAction = QtGui.QAction("添加分类", menu)
            addFolderAction.triggered.connect(lambda checked=False: self.addFolderTriggered.emit())
            menu.addAction(addFolderAction)
            addFileAction = QtGui.QAction("添加功能", menu)
            addFileAction.triggered.connect(lambda checked=False: self.addFileTriggered.emit())
            menu.addAction(addFileAction)
            expendAllAction = QtGui.QAction("展开全部", menu)
            expendAllAction.triggered.connect(lambda checked=False: self.expandAll())
            menu.addAction(expendAllAction)
            collapseAllAction = QtGui.QAction("收起全部", menu)
            collapseAllAction.triggered.connect(lambda checked=False: self.collapseAll())
            menu.addAction(collapseAllAction)
        elif isinstance(widget, EditorTreeWidgetItemWidgetFolder):
            menu = QtWidgets.QMenu()
            addFolderOnFolderAction = QtGui.QAction("添加分类", menu)
            addFolderOnFolderAction.triggered.connect(lambda checked=False, item=item: self.addFolderOnFolderTriggered.emit(item))
            menu.addAction(addFolderOnFolderAction)
            addFileOnFolderAction = QtGui.QAction("添加功能", menu)
            addFileOnFolderAction.triggered.connect(lambda checked=False, item=item: self.addFileOnFolderTriggered.emit(item))
            menu.addAction(addFileOnFolderAction)
            changeNameAction = QtGui.QAction("重命名", menu)
            changeNameAction.triggered.connect(lambda checked=False, widget=widget: widget.setModifyMode())
            menu.addAction(changeNameAction)
            deleteFolderAction = QtGui.QAction("删除", menu)
            deleteFolderAction.triggered.connect(lambda checked=False, item=item: self.deleteFolderTriggered.emit(item))
            menu.addAction(deleteFolderAction)
        elif isinstance(widget, EditorTreeWidgetItemWidgetFile):
            menu = QtWidgets.QMenu()
            runFileAction = QtGui.QAction("运行", menu)
            runFileAction.triggered.connect(lambda checked=False, item=item: self.runFileTriggered.emit(item))
            menu.addAction(runFileAction)
            changeNameAction = QtGui.QAction("重命名", menu)
            changeNameAction.triggered.connect(lambda checked=False, widget=widget: widget.setModifyMode())
            menu.addAction(changeNameAction)
            deleteFileAction = QtGui.QAction("删除", menu)
            deleteFileAction.triggered.connect(lambda checked=False, item=item: self.deleteFileTriggered.emit(item))
            menu.addAction(deleteFileAction)
        else:
            return
        menu.exec(QtGui.QCursor.pos())

    def expand(self, item):
        self.expandItem()
        self.collapseItem()

    def addFolder(self, name: Name, folder: EditorTreeWidgetItem = None) -> EditorTreeWidgetItem:
        item = self.createFolder(name, folder)
        self.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        return item

    def createFolder(self, name: Name, folder: EditorTreeWidgetItem = None) -> EditorTreeWidgetItem:
        item = EditorTreeWidgetItemFolder()
        item.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ChildIndicatorPolicy.ShowIndicator)  # 始终显示折叠按钮
        if folder is None:
            self.addTopLevelItem(item)
        else:
            folder.addChild(item)

        widget = EditorTreeWidgetItemWidgetFolder(name)
        widget.nameChange.connect(lambda event, item=item: self.folderNameChanged.emit(item, event))
        widget.mouseDoubleClicked.connect(lambda event, item=item: self.collapseItem(item) if item.isExpanded() else self.expandItem(item))
        self.setItemWidget(item, 0, widget)

        return item

    def addFile(self, name: Name, folder: EditorTreeWidgetItem = None) -> EditorTreeWidgetItem:
        item = self.createFile(name, folder)
        self.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)
        return item

    def createFile(self, name: Name, folder: EditorTreeWidgetItem = None) -> EditorTreeWidgetItem:
        item = EditorTreeWidgetItemFile()
        item.setChildIndicatorPolicy(QtWidgets.QTreeWidgetItem.ChildIndicatorPolicy.DontShowIndicator)  # 不显示折叠按钮
        if folder is None:
            self.addTopLevelItem(item)
        else:
            folder.addChild(item)

        widget = EditorTreeWidgetItemWidgetFile(name)
        widget.nameChange.connect(lambda event, item=item: self.fileNameChanged.emit(item, event))
        widget.mouseDoubleClicked.connect(lambda event, item=item: self.openFileTriggered.emit(item))
        self.setItemWidget(item, 0, widget)

        return item
