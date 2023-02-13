from PySide6 import QtWidgets


class ScreenTabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent):
        super(ScreenTabWidget, self).__init__(parent)
        self.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.tabBar().hide()
