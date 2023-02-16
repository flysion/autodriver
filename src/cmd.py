import time
from typing import Union

from PySide6 import QtGui, QtCore

import mycmd
import utils
from Device import Device


class Point:
    def __init__(self, image: QtGui.QImage, point: QtCore.QPoint):
        self._image = image
        self._point = point

    def image(self):
        return self._image

    def point(self):
        return self._point


class Rect:
    def __init__(self, image: QtGui.QImage, rect: QtCore.QRect):
        self._image = image
        self._rect = rect

    def image(self):
        return self._image

    def rect(self):
        return self._rect


@mycmd.command()
def wait(context: mycmd.Context, ms: int):
    time.sleep(ms / 1000)


@mycmd.command()
def move(context: mycmd.Context, p1: Point, p2: Point):
    context.move(p1.point().x(), p1.point().y(), p2.point().x(), p2.point().y())


@mycmd.command()
def moven(context: mycmd.Context, x1: int, y1: int, x2: int, y2: int):
    context.move(x1, y1, x2, y2)


@mycmd.command()
def click(context: mycmd.Context, p: Union[Point, Rect]):
    if isinstance(p, Point):
        context.click(p.point().x(), p.point().y())
    elif isinstance(p, Rect):
        context.click(p.rect().center().x(), p.rect().center().y())


@mycmd.command()
def click_if(context: mycmd.Context, p: Rect, sameness=100):
    rect = p.rect()
    image1 = p.image().copy(rect)
    image2 = context['screen'].copy(rect)
    if utils.qimage_sameness(image1, image2) >= sameness:
        context.click(rect.center().x(), rect.center().y())


def run(device: Device, values: dict, reader, mainFile, callback=None) -> int:
    _screen = device.screen()

    def click(x: int, y: int):
        device.click(x, y)

    def move(x1: int, y1: int, x2: int, y2: int):
        device.move(x1, y1, x2, y2)

    def refresh():
        nonlocal _screen
        _screen = device.screen()

    commands = {
        'refresh': lambda context: refresh()
    }

    context = mycmd.Context()
    context.click = click
    context.move = move
    context['screen'] = lambda: _screen

    return mycmd.run(mainFile, reader, context, values=values, commands=commands, exec_callback=callback)
