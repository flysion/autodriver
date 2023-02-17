import numpy
from PySide6 import QtCore, QtGui

DIRECT_NONE = 0
DIRECT_TOP = 1
DIRECT_RIGHT = 2
DIRECT_BOTTOM = 4
DIRECT_LEFT = 8
DIRECT_TOP_LEFT = DIRECT_TOP | DIRECT_LEFT
DIRECT_TOP_RIGHT = DIRECT_TOP | DIRECT_RIGHT
DIRECT_BOTTOM_LEFT = DIRECT_BOTTOM | DIRECT_LEFT
DIRECT_BOTTOM_RIGHT = DIRECT_BOTTOM | DIRECT_RIGHT


def pointInRectDirect(pos: QtCore.QPointF, rect: QtCore.QRectF, near: int = 10) -> int:
    topLeft = pos - rect.topLeft()
    bottomRight = rect.bottomRight() - pos
    direct = DIRECT_NONE

    if topLeft.x() <= near:
        direct = direct | DIRECT_LEFT

    if topLeft.y() <= near:
        direct = direct | DIRECT_TOP

    if bottomRight.x() <= near:
        direct = direct | DIRECT_RIGHT

    if bottomRight.y() <= near:
        direct = direct | DIRECT_BOTTOM

    return direct


def directToCursorSizeStyle(direct):
    if direct == DIRECT_TOP_LEFT or direct == DIRECT_BOTTOM_RIGHT:
        return QtCore.Qt.CursorShape.SizeFDiagCursor
    elif direct == DIRECT_BOTTOM_LEFT or direct == DIRECT_TOP_RIGHT:
        return QtCore.Qt.CursorShape.SizeBDiagCursor
    elif direct == DIRECT_TOP or direct == DIRECT_BOTTOM:
        return QtCore.Qt.CursorShape.SizeVerCursor
    elif direct == DIRECT_LEFT or direct == DIRECT_RIGHT:
        return QtCore.Qt.CursorShape.SizeHorCursor
    else:
        return None
