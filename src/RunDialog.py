from PySide6 import QtWidgets, QtCore, QtGui

import executor
import thread
from Device import Device
from RunDialogUI import Ui_RunDialog


class RunDialog(QtWidgets.QDialog):
    exec = QtCore.Signal(object, object, object, object)
    refresh = QtCore.Signal(QtGui.QImage)
    clicked = QtCore.Signal(int, int)
    touched = QtCore.Signal(int, int, int, int)
    print = QtCore.Signal(str)

    def __init__(self, parent, device: Device, values: dict, reader, mainFile):
        super(RunDialog, self).__init__(parent=parent)
        self.ui = Ui_RunDialog()
        self.ui.setupUi(self)

        self._device = device
        self._values = values
        self._reader = reader
        self._mainFile = mainFile
        self._status = 0
        self._thread = None

        self._scene = QtWidgets.QGraphicsScene(self)
        self.ui.graphicsView.setScene(self._scene)
        self.ui.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._screenImage = None
        self._screenItem = None

        self.ui.runButton.clicked.connect(self.on_runButton_clicked)
        self.exec.connect(self.on_exec)
        self.refresh.connect(self.on_refresh)
        self.clicked.connect(self.on_clicked)
        self.touched.connect(self.on_touched)
        self.print.connect(self.on_print)

    def setSceneImage(self, image: QtGui.QImage):
        self._screenImage = image
        if self._screenItem is None:
            self._screenItem = self._scene.addPixmap(QtGui.QPixmap.fromImage(image))
        else:
            self._screenItem.setPixmap(QtGui.QPixmap.fromImage(image))

        self._scene.setSceneRect(0, 0, self._screenImage.width(), self._screenImage.height())
        self.adjustGraphicsViewSize()

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        if self._screenImage is not None:
            self.adjustGraphicsViewSize()

    def adjustGraphicsViewSize(self):
        scale = self.ui.graphicsView.height() / self._screenImage.height()
        transform = self.ui.graphicsView.transform()
        transform = QtGui.QTransform(scale, transform.m12(), transform.m21(), scale, transform.dx(), transform.dy())
        self.ui.graphicsView.setTransform(transform)

        self.ui.graphicsView.setMaximumWidth(self._screenImage.width() * scale)

    def quit(self):
        return self._status == 2

    def sleep(self, second):
        self._thread.sleep(second)

    #
    # def screenClick(self, x, y):
    #     transform = self.ui.graphicsView.transform()
    #     width = transform.m11() * self._screenImage.width() * 0.02  # 通过缩放比例显示点的大小
    #     height = transform.m22() * self._screenImage.width() * 0.02  # 通过缩放比例显示点的大小
    #     topLeft = self.ui.graphicsView.mapToScene(QtCore.QPoint(x - width, y - height))
    #     bottomRight = self.mapToScene(QtCore.QPoint(x + width, y + height))
    #     item = self.ui.graphicsView.screen().addEllipse()

    def createExecThread(self):
        return thread.Async(executor.exec, self._device, self._values, self._reader, self._mainFile,
                            loop=self.ui.loopCheckBox.isChecked(), quit=self.quit, sleep=self.sleep,
                            print_fn=lambda s: self.print.emit(s),
                            exec_callback=lambda *args: self.exec.emit(*args),
                            refresh_callback=lambda screen: self.refresh.emit(screen),
                            click_callback=lambda x, y: self.clicked.emit(x, y),
                            touch_callback=lambda x1, y1, x2, y2: self.touched.emit(x1, y1, x2, y2))

    def on_clicked(self, x, y):
        self.ui.plainTextEdit.appendPlainText(f"click {x},{y}")

    def on_touched(self, x1, y1, x2, y2):
        self.ui.plainTextEdit.appendPlainText(f"touch {x1},{y1},{x2},{y2}")

    def on_refresh(self, image: QtGui.QImage):
        self.setSceneImage(image)

    def on_exec(self, context, file, fragment, result):
        if fragment['type'] == 'command':
            self.ui.plainTextEdit.appendPlainText(f"command {fragment['name']} {file.path()}:{fragment['lineno']}")

    def on_print(self, s):
        self.ui.plainTextEdit.appendPlainText(s)

    def on_runButton_clicked(self):
        if self._status == 0:
            self._status = 1
            self._thread = self.createExecThread()
            self._thread.finished.connect(self.on_thread_finished)
            self._thread.start()
            self.ui.runButton.setText("停止")
            self.ui.loopCheckBox.setDisabled(True)
        elif self._status == 1:
            self._status = 2
            self.ui.runButton.setDisabled(True)
            self.ui.runButton.setText("停止中...")

    def on_thread_finished(self):
        self.ui.runButton.setDisabled(False)
        self.ui.loopCheckBox.setDisabled(False)
        self.ui.runButton.setText("运行")
        self._status = 0
        del self._thread
