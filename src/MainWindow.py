# coding: utf-8
import os.path
import pickle
from typing import Union, Tuple

from PySide6 import QtWidgets, QtGui, QtCore

import executor
from Counter import Counter
from Device import Device
from EditorTabView import EditorTabView
from EditorTree import EditorTreeWidgetItemFile, EditorTreeWidgetItemFolder, EditorTreeWidgetItemNameChangeEvent
from MainWindowUI import Ui_MainWindow
from Name import Name
from RunDialog import RunDialog
from ScreenGraphics import ScreenGraphicsView, ScreenGraphicsItemRect, ScreenGraphicsItemPoint
from ScreenList import ScreenListWidgetItem
from ScreenTree import ScreenTreeWidgetItemGroup, ScreenTreeWidgetItemScene, ScreenTreeWidgetItemElement, ScreenTreeWidgetItem, ScreenTreeWidgetItemNameChangeEvent

ScreenGraphicsItem = Union[ScreenGraphicsItemRect, ScreenGraphicsItemPoint]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, device: Device, file=None):
        super(MainWindow, self).__init__()

        self._device = device
        self._counter = Counter()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.openMenu.triggered.connect(self.on_openMenu_triggered)
        self.ui.saveMenu.triggered.connect(self.on_saveMenu_triggered)
        self.ui.newMenu.triggered.connect(self.on_newMenu_triggered)

        self.ui.screenListWidget.currentItemChanged.connect(self.on_screenListWidget_currentItemChanged)

        self.ui.screenTreeWidget.currentItemChanged.connect(self.on_screenTreeWidget_currentItemChanged)
        self.ui.screenTreeWidget.addGroupTriggered.connect(self.on_screenTreeWidget_addGroupTriggered)
        self.ui.screenTreeWidget.addSceneOnGroupTriggered.connect(self.on_screenTreeWidget_addSceneOnGroupTriggered)
        self.ui.screenTreeWidget.deleteGroupTriggered.connect(self.on_screenTreeWidget_deleteGroupTriggered)
        self.ui.screenTreeWidget.deleteSceneTriggered.connect(self.on_screenTreeWidget_deleteSceneTriggered)
        self.ui.screenTreeWidget.deleteElementTriggered.connect(self.on_screenTreeWidget_deleteElementTriggered)
        self.ui.screenTreeWidget.reloadSceneImageTriggered.connect(self.on_screenTreeWidget_reloadSceneImageTriggered)
        self.ui.screenTreeWidget.groupNameChanged.connect(self.on_screenTreeWidget_groupNameChanged)
        self.ui.screenTreeWidget.sceneNameChanged.connect(self.on_screenTreeWidget_sceneNameChanged)
        self.ui.screenTreeWidget.elementNameChanged.connect(self.on_screenTreeWidget_elementNameChanged)

        self.ui.editorTreeWidget.addFolderTriggered.connect(self.on_editorTreeWidget_addFolderTriggered)
        self.ui.editorTreeWidget.addFileTriggered.connect(self.on_editorTreeWidget_addFileTriggered)
        self.ui.editorTreeWidget.addFolderOnFolderTriggered.connect(self.on_editorTreeWidget_addFolderTriggered)
        self.ui.editorTreeWidget.addFileOnFolderTriggered.connect(self.on_editorTreeWidget_addFileTriggered)
        self.ui.editorTreeWidget.openFileTriggered.connect(self.on_editorTreeWidget_openFileTriggered)
        self.ui.editorTreeWidget.deleteFolderTriggered.connect(self.on_editorTreeWidget_deleteFolderTriggered)
        self.ui.editorTreeWidget.deleteFileTriggered.connect(self.on_editorTreeWidget_deleteFileTriggered)
        self.ui.editorTreeWidget.folderNameChanged.connect(self.on_editorTreeWidget_folderNameChanged)
        self.ui.editorTreeWidget.fileNameChanged.connect(self.on_editorTreeWidget_fileNameChanged)
        self.ui.editorTreeWidget.runFileTriggered.connect(self.on_editorTreeWidget_runFileTriggered)

        self._file = None
        if file is not None:
            self.open(file)

    def serializeData(self):
        screenTreeItems = []
        for i in range(self.ui.screenTreeWidget.topLevelItemCount()):
            screenTreeWidgetItemGroup = self.ui.screenTreeWidget.topLevelItem(i)
            groupItem = dict(name=screenTreeWidgetItemGroup.name(), children=[])
            for s in range(screenTreeWidgetItemGroup.childCount()):
                screenTreeWidgetItemScene = screenTreeWidgetItemGroup.child(s)
                screenImageBuffer = QtCore.QBuffer()
                screenImageBuffer.open(QtCore.QIODevice.OpenModeFlag.ReadWrite)
                screenTreeWidgetItemScene.graphicsView().sceneImage().save(screenImageBuffer, "png")
                sceneItem = dict(name=screenTreeWidgetItemScene.name(), image=screenImageBuffer.data(), children=[])
                for j in range(screenTreeWidgetItemScene.childCount()):
                    screenTreeWidgetItemElement = screenTreeWidgetItemScene.child(j)
                    if isinstance(screenTreeWidgetItemElement.graphicsItem(), ScreenGraphicsItemRect):
                        rect = screenTreeWidgetItemElement.graphicsItem().mapRectToScene(screenTreeWidgetItemElement.graphicsItem().rect())
                        elementItem = dict(name=screenTreeWidgetItemElement.name(), type=1, rect=(rect.x(), rect.y(), rect.width(), rect.height()))
                    else:
                        point = screenTreeWidgetItemElement.graphicsItem().mapToScene(screenTreeWidgetItemElement.graphicsItem().rect().center())
                        elementItem = dict(name=screenTreeWidgetItemElement.name(), type=2, point=(point.x(), point.y()))
                    sceneItem['children'].append(elementItem)
                groupItem['children'].append(sceneItem)
            screenTreeItems.append(groupItem)

        def forEditorTreeItem(parent: EditorTreeWidgetItemFolder = None, key: str = None):
            items = []
            for i in range(self.ui.editorTreeWidget.topLevelItemCount() if parent is None else parent.childCount()):
                child = self.ui.editorTreeWidget.topLevelItem(i) if parent is None else parent.child(i)
                if isinstance(child, EditorTreeWidgetItemFolder):
                    item = dict(name=child.name(), type=1, children=forEditorTreeItem(child, key))
                else:
                    item = dict(name=child.name(), type=2, textCode=child.textCode())
                items.append(item)
            return items

        data = dict(counter=dict(start=self._counter.start(), step=self._counter.step()), version=1,
                    screenTreeItems=screenTreeItems, editorTreeItems=forEditorTreeItem())
        return pickle.dumps(data)

    def unserializeData(self, data):
        data = pickle.loads(data)

        self._counter = Counter(**data['counter'])

        for groupItem in data['screenTreeItems']:
            screenTreeWidgetItemGroup = self.createScreenGroup(groupItem['name'])
            for sceneItem in groupItem['children']:
                image = QtGui.QImage.fromData(sceneItem['image'])
                screenTreeWidgetItemScene, screenGraphicsView, screenListWidgetItem = self.createScreenScene(sceneItem['name'], image, screenTreeWidgetItemGroup)
                for elementItem in sceneItem['children']:
                    if elementItem['type'] == 1:
                        rect = QtCore.QRectF(*elementItem['rect'])
                        screenGraphicsItem = screenGraphicsView.createRectItem(elementItem['name'], rect)
                    else:
                        point = QtCore.QPoint(*elementItem['point'])
                        screenGraphicsItem = screenGraphicsView.createPointItem(elementItem['name'], point)
                    self.createScreenElement(elementItem['name'], screenGraphicsView, screenGraphicsItem)

        def forEditorTreeItem(items, parentEditorTreeWidgetItem: EditorTreeWidgetItemFolder = None):
            for item in items:
                if item['type'] == 1:
                    editorTreeWidgetItem = self.ui.editorTreeWidget.createFolder(item['name'], parentEditorTreeWidgetItem)
                    forEditorTreeItem(item['children'], editorTreeWidgetItem)
                elif item['type'] == 2:
                    editorTreeWidgetItem = self.ui.editorTreeWidget.createFile(item['name'], parentEditorTreeWidgetItem)
                    self.editorTextChanged(item['textCode'], editorTreeWidgetItem)

        forEditorTreeItem(data['editorTreeItems'])
        self.ui.editorTreeWidget.sortItems(0, QtCore.Qt.SortOrder.AscendingOrder)

    def reset(self):
        self.ui.screenTabWidget.clear()
        self.ui.screenListWidget.clear()
        self.ui.screenTreeWidget.clear()

    def open(self, file):
        with open(file, 'rb') as f:
            self.unserializeData(f.read())
        self._file = file
        self.setWindowTitle('{name}({dir})'.format(name=os.path.basename(file), dir=file))

    def save(self, file):
        data = self.serializeData()
        with open(file, 'wb') as f:
            f.write(data)
        self._file = file
        self.setWindowTitle('{name}({dir})'.format(name=os.path.basename(file), dir=file))

    def on_openMenu_triggered(self, checked=False):
        file, ext = QtWidgets.QFileDialog.getOpenFileName(self, "打开文件", ".", "(*.ddi)")
        if file != '':
            self.reset()
            self.open(file)

    def on_saveMenu_triggered(self, checked=False):
        if self._file is None:
            file, ext = QtWidgets.QFileDialog.getSaveFileName(self, "保存文件", ".", "(*.ddi)")
            if file != '':
                self.save(file)
        else:
            self.save(self._file)

    def on_newMenu_triggered(self, checked=False):
        self._file = None
        self.ui.screenTabWidget.clear()
        self.ui.screenListWidget.clear()
        self.ui.screenTreeWidget.clear()
        self.ui.editorTreeWidget.clear()
        self.ui.editorTabWidget.clear()

    def on_editorTreeWidget_addFolderTriggered(self, parent: EditorTreeWidgetItemFolder = None):
        self.ui.editorTreeWidget.addFolder(Name("新建分类"), parent)

    def on_editorTreeWidget_addFileTriggered(self, parent: EditorTreeWidgetItemFolder = None):
        name = Name("新建功能", id=f"f{self._counter.next()}")
        self.ui.editorTreeWidget.addFile(name, parent)

    def on_editorTreeWidget_openFileTriggered(self, editorTreeWidgetItem: EditorTreeWidgetItemFile):
        if editorTreeWidgetItem.tabView() is None:  # 创建编辑器
            editorTabView = EditorTabView(text=editorTreeWidgetItem.textCode())
            self.ui.editorTabWidget.addTab(editorTabView, editorTreeWidgetItem.name())
            editorTabView.textChanged.connect(lambda text, editorTreeWidgetItem=editorTreeWidgetItem: self.editorTextChanged(text, editorTreeWidgetItem))
            editorTreeWidgetItem.setTabView(editorTabView)
            editorTabView.setTreeItem(editorTreeWidgetItem)
        elif self.ui.editorTabWidget.indexOf(editorTreeWidgetItem.tabView()) == -1:  # 已有编辑器（曾经创建过，后来关闭了）
            editorTabView = editorTreeWidgetItem.tabView()
            self.ui.editorTabWidget.addTab(editorTabView, editorTreeWidgetItem.name())
        self.ui.editorTabWidget.setCurrentWidget(editorTreeWidgetItem.tabView())

    def on_editorTreeWidget_deleteFolderTriggered(self, editorTreeWidgetItem: EditorTreeWidgetItemFolder):
        # 移除tab中打开的文件
        for itemIter in QtWidgets.QTreeWidgetItemIterator(self.ui.editorTreeWidget):
            item = itemIter.value()
            if not isinstance(item, EditorTreeWidgetItemFile):
                continue
            if item.tabView() is not None:
                self.ui.editorTabWidget.removeTabByWidget(item.tabView())
        self.ui.editorTreeWidget.removeItem(editorTreeWidgetItem)

    def on_editorTreeWidget_deleteFileTriggered(self, editorTreeWidgetItem: EditorTreeWidgetItemFile):
        self.ui.editorTreeWidget.removeItem(editorTreeWidgetItem)
        if editorTreeWidgetItem.tabView() is not None:
            self.ui.editorTabWidget.removeTabByWidget(editorTreeWidgetItem.tabView())

    def on_editorTreeWidget_folderNameChanged(self, editorTreeWidgetItem: EditorTreeWidgetItemFolder, event: EditorTreeWidgetItemNameChangeEvent):
        event.accept()

    def on_editorTreeWidget_fileNameChanged(self, editorTreeWidgetItem: EditorTreeWidgetItemFile, event: EditorTreeWidgetItemNameChangeEvent):
        event.accept()
        if editorTreeWidgetItem.tabView() is not None:
            index = self.ui.editorTabWidget.indexOf(editorTreeWidgetItem.tabView())
            if index != -1:
                self.ui.editorTabWidget.setTabText(index, event.name())

    def on_editorTreeWidget_runFileTriggered(self, editorTreeWidgetItem: EditorTreeWidgetItemFile):
        files = {}
        values = {}

        for itemIter in QtWidgets.QTreeWidgetItemIterator(self.ui.editorTreeWidget):
            item = itemIter.value()
            if not isinstance(item, EditorTreeWidgetItemFile):
                continue
            files[item.name().id()] = item.textCode()
            values[item.name().id()] = item

        for itemIter in QtWidgets.QTreeWidgetItemIterator(self.ui.screenTreeWidget):
            item = itemIter.value()
            if not isinstance(item, ScreenTreeWidgetItemElement):
                continue
            elementName = item.name()
            rect: QtCore.QRectF = item.graphicsItem().mapRectToScene(item.graphicsItem().rect())
            if isinstance(item.graphicsItem(), ScreenGraphicsItemPoint):
                values[elementName.id()] = executor.Point(item.parent().graphicsView().sceneImage(), rect.center().toPoint())
            else:
                values[elementName.id()] = executor.Rect(item.parent().graphicsView().sceneImage(), rect.toRect())

        def reader(file: EditorTreeWidgetItemFile, files=files):
            if file.name().id() in files:
                return files[file.name().id()]
            # TODO 文件不存在

        dialog = RunDialog(self, self._device, values, reader, editorTreeWidgetItem)
        dialog.exec()

    def on_screenGraphicsView_sizeChange(self, width: int, height: int):
        self.ui.widget_1.setMinimumWidth(width)
        self.ui.widget_1.setMaximumWidth(width)

    def on_screenTreeWidget_addGroupTriggered(self):
        screenTreeWidgetItemGroup = self.createScreenGroup(Name("新建分组"))
        self.ui.screenTreeWidget.setCurrentItem(screenTreeWidgetItemGroup)

    def on_screenTreeWidget_addSceneOnGroupTriggered(self, screenTreeWidgetItemGroup: ScreenTreeWidgetItemGroup):
        screenTreeWidgetItemScene, screenGraphicsView, screenListWidgetItem = self.createScreenScene(Name("新建场景"), self._device.screen(), screenTreeWidgetItemGroup)
        self.ui.screenTabWidget.setCurrentWidget(screenGraphicsView)
        self.ui.screenListWidget.setCurrentItem(screenListWidgetItem)
        self.ui.screenTreeWidget.setCurrentItem(screenTreeWidgetItemScene)

    def on_screenGraphicsView_addedElement(self, screenGraphicsView: ScreenGraphicsView, name: Name, screenGraphicsItem: ScreenGraphicsItem):
        screenTreeWidgetItemElement, _ = self.createScreenElement(name, screenGraphicsView, screenGraphicsItem)
        # self.ui.screenTreeWidget.setCurrentItem(screenTreeWidgetItemElement)

    def on_screenTreeWidget_deleteGroupTriggered(self, screenTreeWidgetItemGroup: ScreenTreeWidgetItemGroup):
        for i in range(screenTreeWidgetItemGroup.childCount()):
            screenTreeWidgetItemScene = screenTreeWidgetItemGroup.child(i)
            self.ui.screenListWidget.takeItem(self.ui.screenListWidget.row(screenTreeWidgetItemScene.listItem()))
            self.ui.screenTabWidget.removeTab(self.ui.screenTabWidget.indexOf(screenTreeWidgetItemScene.graphicsView()))
        self.ui.screenTreeWidget.takeTopLevelItem(self.ui.screenTreeWidget.indexOfTopLevelItem(screenTreeWidgetItemGroup))

    def on_screenTreeWidget_groupNameChanged(self, screenTreeWidgetItemGroup: ScreenTreeWidgetItemGroup, event: ScreenTreeWidgetItemNameChangeEvent):
        event.accept()

    def on_screenTreeWidget_deleteSceneTriggered(self, screenTreeWidgetItemScene: ScreenTreeWidgetItemScene):
        self.ui.screenListWidget.takeItem(self.ui.screenListWidget.row(screenTreeWidgetItemScene.listItem()))
        self.ui.screenTabWidget.removeTab(self.ui.screenTabWidget.indexOf(screenTreeWidgetItemScene.graphicsView()))
        screenTreeWidgetItemScene.parent().removeChild(screenTreeWidgetItemScene)

    def on_screenTreeWidget_reloadSceneImageTriggered(self, screenTreeWidgetItemScene: ScreenTreeWidgetItemScene):
        qimage = self._device.screen()
        screenTreeWidgetItemScene.graphicsView().setSceneImage(qimage)
        screenTreeWidgetItemScene.listItem().setImage(qimage)

    def on_screenTreeWidget_sceneNameChanged(self, screenTreeWidgetItemScene: ScreenTreeWidgetItemScene, event: ScreenTreeWidgetItemNameChangeEvent):
        event.accept()

    def on_screenTreeWidget_deleteElementTriggered(self, screenTreeWidgetItemElement: ScreenTreeWidgetItemElement):
        screenTreeWidgetItemElement.graphicsItem().scene().removeItem(screenTreeWidgetItemElement.graphicsItem())
        screenTreeWidgetItemElement.parent().removeChild(screenTreeWidgetItemElement)

    def on_screenTreeWidget_elementNameChanged(self, screenTreeWidgetItemElement: ScreenTreeWidgetItemElement, event: ScreenTreeWidgetItemNameChangeEvent):
        screenTreeWidgetItemElement.graphicsItem().setToolTip(event.name())
        event.accept()

    def on_screenTreeWidget_currentItemChanged(self, currentTreeItem: ScreenTreeWidgetItem, previousTreeItem: ScreenTreeWidgetItem):
        if currentTreeItem is None:
            return
        if isinstance(currentTreeItem, ScreenTreeWidgetItemScene):
            self.ui.screenTabWidget.setCurrentWidget(currentTreeItem.graphicsView())
            self.ui.screenListWidget.setCurrentItem(currentTreeItem.listItem())
        elif isinstance(currentTreeItem, ScreenTreeWidgetItemElement):
            self.ui.screenTabWidget.setCurrentWidget(currentTreeItem.parent().graphicsView())
            self.ui.screenListWidget.setCurrentItem(currentTreeItem.parent().listItem())
            currentTreeItem.graphicsItem().light()

    def on_screenListWidget_currentItemChanged(self, currentListItem: ScreenListWidgetItem, previousListItem: ScreenListWidgetItem):
        if currentListItem is None:
            return
        self.ui.screenTabWidget.setCurrentWidget(currentListItem.graphicsView())
        self.ui.screenTreeWidget.setCurrentItem(currentListItem.treeItem())

    def editorTextChanged(self, text: str, editorTreeWidgetItem: EditorTreeWidgetItemFile):
        editorTreeWidgetItem.setTextCode(text)

    def createScreenGroup(self, name: Name) -> ScreenTreeWidgetItemGroup:
        return self.ui.screenTreeWidget.addGroupItem(name)

    def createScreenScene(self, name: Name, image: QtGui.QImage, screenTreeWidgetItemGroup: ScreenTreeWidgetItemGroup) \
            -> Tuple[ScreenTreeWidgetItemScene, ScreenGraphicsView, ScreenListWidgetItem]:
        screenGraphicsView = ScreenGraphicsView(self._counter, self)
        screenGraphicsView.sizeChanged.connect(self.on_screenGraphicsView_sizeChange)
        screenGraphicsView.addedElement.connect(self.on_screenGraphicsView_addedElement)
        screenGraphicsView.clickRequested.connect(lambda p: self.deviceClick(p))
        screenGraphicsView.moveRequested.connect(lambda p, p1: self.deviceMove(p, p1))
        screenGraphicsView.setSceneImage(image)
        self.ui.screenTabWidget.addTab(screenGraphicsView, name)

        listItem = ScreenListWidgetItem(image)
        self.ui.screenListWidget.addItem(listItem)

        treeItem = self.ui.screenTreeWidget.addSceneItem(name, screenTreeWidgetItemGroup)

        screenGraphicsView.setListItem(listItem)
        screenGraphicsView.setTreeItem(treeItem)
        listItem.setGraphicsView(screenGraphicsView)
        listItem.setTreeItem(treeItem)
        treeItem.setGraphicsView(screenGraphicsView)
        treeItem.setListItem(listItem)

        return treeItem, screenGraphicsView, listItem

    def createScreenElement(self, name: Name, screenGraphicsView: ScreenGraphicsView, screenGraphicsItem: ScreenGraphicsItem) \
            -> Tuple[ScreenTreeWidgetItemElement, ScreenGraphicsItem]:
        treeItem = self.ui.screenTreeWidget.addElementItem(name, screenGraphicsView.treeItem())
        treeItem.setGraphicsItem(screenGraphicsItem)
        screenGraphicsItem.setTreeItem(treeItem)
        return treeItem, screenGraphicsItem

    def deviceClick(self, p: QtCore.QPoint):
        self._device.click(p.x(), p.y())
        self.ui.statusbar.showMessage(f"点击屏幕({p.x()},{p.y()})", 2000)

    def deviceMove(self, p: QtCore.QPoint, p1: QtCore.QPoint):
        self._device.move(p.x(), p.y(), p1.x(), p1.y())
        self.ui.statusbar.showMessage(f"滑动屏幕({p.x()},{p.y()} -> {p1.x()},{p1.y()})", 2000)
