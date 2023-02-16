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


def qimage2opencv(qimage: QtGui.QImage):
    cvimage = numpy.zeros((qimage.height(), qimage.width(), 3), dtype=numpy.uint8)
    for y in range(0, qimage.height()):
        for x in range(0, qimage.width()):
            r = QtGui.qRed(qimage.pixel(x, y))
            g = QtGui.qGreen(qimage.pixel(x, y))
            b = QtGui.qBlue(qimage.pixel(x, y))
            cvimage[x, y, 0] = r
            cvimage[x, y, 1] = g
            cvimage[x, y, 2] = b
    return cvimage


def qimage_sameness(image1: QtGui.QImage, image2: QtGui.QImage) -> int:
    a = 0
    b = 0

    for x in range(image1.width()):
        for y in range(image1.height()):
            color1: QtGui.QColor = image1.pixelColor(x, y)
            color2: QtGui.QColor = image2.pixelColor(x, y)
            if color1.red() == color2.red() and color1.green() == color2.green() and color1.blue() == color2.blue():
                a += 1
            else:
                b += 1

    return int(a / (a + b) * 100)
