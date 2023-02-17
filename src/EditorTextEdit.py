from PySide6 import QtWidgets, QtGui, QtCore


class EditorLineNumberArea(QtWidgets.QWidget):
    def __init__(self, textEditor: 'EditorTextEdit'):
        super(EditorLineNumberArea, self).__init__(textEditor)
        self._textEditor = textEditor

    def sizeHint(self):
        return QtCore.QSize(self._textEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self._textEditor.lineNumberAreaPaintEvent(event)


class EditorTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super(EditorTextEdit, self).__init__()
        self._editorLineNumberArea = EditorLineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def paintEvent(self, e: QtGui.QPaintEvent) -> None:
        super(EditorTextEdit, self).paintEvent(e)

    def lineNumberAreaPaintEvent(self, event):
        with QtGui.QPainter(self._editorLineNumberArea) as painter:
            painter.fillRect(event.rect(), QtCore.Qt.lightGray)
            block = self.firstVisibleBlock()
            blockNumber = block.blockNumber()
            offset = self.contentOffset()
            top = self.blockBoundingGeometry(block).translated(offset).top()
            bottom = top + self.blockBoundingRect(block).height()

            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    number = str(blockNumber + 1)
                    painter.setPen(QtCore.Qt.black)
                    width = self._editorLineNumberArea.width() - 5
                    height = self.fontMetrics().height()
                    painter.drawText(0, top, width, height, QtCore.Qt.AlignRight, number)

                block = block.next()
                top = bottom
                bottom = top + self.blockBoundingRect(block).height()
                blockNumber += 1

    def lineNumberAreaWidth(self) -> int:
        digits = 1
        maxLine = max(1, self.blockCount());
        while maxLine >= 10:
            maxLine /= 10
            digits += 1
        return 15 + self.fontMetrics().horizontalAdvance('9') * digits

    def updateLineNumberAreaWidth(self, blockCount: int):
        super(EditorTextEdit, self).setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect: QtCore.QRect, dy: int):
        if dy:
            self._editorLineNumberArea.scroll(0, dy)
        else:
            self._editorLineNumberArea.update(0, rect.y(), self._editorLineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, e: QtGui.QResizeEvent) -> None:
        super(EditorTextEdit, self).resizeEvent(e)
        rect = self.contentsRect()
        self._editorLineNumberArea.setGeometry(QtCore.QRect(rect.left(), rect.top(), self.lineNumberAreaWidth(), rect.height()))

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            lineColor = QtGui.QColor(QtCore.Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)