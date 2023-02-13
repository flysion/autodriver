from PySide6 import QtCore, QtWidgets, QtGui

from EditorLineno import EditorLinenoWidget
from EditorTextEdit import EditorTextEdit
from typing import TYPE_CHECKING


# https://blog.csdn.net/weixin_41102672/article/details/108401204
class EditorTabView(QtWidgets.QWidget):
    if TYPE_CHECKING:
        from EditorTree import EditorTreeWidgetItemFile

    textChanged = QtCore.Signal(str)

    def __init__(self, text=None):
        super(EditorTabView, self).__init__()

        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)

        self._linenoWidget = EditorLinenoWidget()
        self._linenoWidget.setLineCount(1)
        self._layout.addWidget(self._linenoWidget, 0, 0)

        self._font = QtGui.QFont()
        self._font.setPixelSize(15)
        self._font.setFamilies("Consolas")

        self._textEdit = EditorTextEdit()
        self._textEdit.setFont(self._font)
        self._textEdit.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        if text is not None:
            self._textEdit.setPlainText(text)
        self._textEdit.textChanged.connect(self.on_editor_textChanged)
        self._layout.addWidget(self._textEdit, 0, 1)

        self._treeItem = None

    def setTreeItem(self, treeItem: 'EditorTreeWidgetItemFile'):
        self._treeItem = treeItem

    def treeItem(self) -> 'EditorTreeWidgetItemFile':
        return self._treeItem

    def on_editor_textChanged(self):
        self._linenoWidget.setLineCount(self._textEdit.document().lineCount())
        self.textChanged.emit(self._textEdit.toPlainText())
