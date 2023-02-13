from PySide6 import QtWidgets, QtCore, QtGui


class EditorLinenoWidgetItemWidget(QtWidgets.QWidget):
    def __init__(self, lineno: int):
        super(EditorLinenoWidgetItemWidget, self).__init__()

        self._lineno = lineno

        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self._font = QtGui.QFont()
        self._font.setPixelSize(15)
        self._font.setFamilies("Consolas")

        self._label = QtWidgets.QLabel()
        self._label.setFont(self._font)
        self._label.setText("%d " % lineno)
        self._label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignRight)
        self._layout.addWidget(self._label)


class EditorLinenoWidget(QtWidgets.QListWidget):
    def __init__(self):
        super(EditorLinenoWidget, self).__init__()
        # self.setAutoFillBackground(True)
        self.setStyleSheet("background-color:#CCCCCC")
        self.setMaximumWidth(50)
        self.setMinimumWidth(50)
        self.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)  # 去掉边框
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.MultiSelection)  # 多选
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._lineItems = []

    def setLineCount(self, lineCount: int):
        if len(self._lineItems) > lineCount:
            for i in range(lineCount, len(self._lineItems)):
                item, widget = self._lineItems[i]
                self.takeItem(i)
                self.removeItemWidget(item)
                del self._lineItems[i]
                del item
                del widget
        elif len(self._lineItems) < lineCount:
            for i in range(len(self._lineItems), lineCount):
                item = QtWidgets.QListWidgetItem()
                self.addItem(item)
                widget = EditorLinenoWidgetItemWidget(i + 1)
                self.setItemWidget(item, widget)
                self._lineItems.append((item, widget))
