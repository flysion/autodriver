import time
from typing import Union, Tuple

import cv2
import numpy
from PySide6 import QtGui, QtCore

import mycmd
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
def run_if(context: mycmd.Context, pos: Rect, file, same: int = 80):
    if screen_sameness(context['screen'], pos) >= same:
        context.load(file)


@mycmd.command()
def run_unless(context: mycmd.Context, pos: Rect, file, same: int = 80):
    if screen_sameness(context['screen'], pos) < same:
        context.load(file)


@mycmd.command()
def exit_if(context: mycmd.Context, pos: Rect, code: int = 0, same: int = 80):
    if screen_sameness(context['screen'], pos) >= same:
        context.exit(code)


@mycmd.command()
def exit_unless(context: mycmd.Context, pos: Rect, code: int = 0, same: int = 80):
    if screen_sameness(context['screen'], pos) < same:
        context.exit(code)


@mycmd.command()
def goto_if(context: mycmd.Context, pos: Rect, label: mycmd.Label, same: int = 80):
    if screen_sameness(context['screen'], pos) >= same:
        context.goto(label)


@mycmd.command()
def goto_unless(context: mycmd.Context, pos: Rect, label: mycmd.Label, same: int = 80):
    if screen_sameness(context['screen'], pos) < same:
        context.goto(label)


@mycmd.command()
def wait(context: mycmd.Context, ms: int):
    time.sleep(ms / 1000)


@mycmd.command()
def wait_if(context: mycmd.Context, pos: Rect, same: int = 80, ms: int = 300):
    if screen_sameness(context['screen'], pos) >= same:
        time.sleep(ms / 1000)


@mycmd.command()
def wait_unless(context: mycmd.Context, pos: Rect, same: int = 80, ms: int = 300):
    if screen_sameness(context['screen'], pos) < same:
        time.sleep(ms / 1000)


@mycmd.command()
def refresh_if(context: mycmd.Context, pos: Rect, same: int = 80, ms: int = 300):
    if screen_sameness(context.refresh(), pos) >= same:
        time.sleep(ms / 1000)


@mycmd.command()
def refresh_unless(context: mycmd.Context, pos: Rect, same: int = 80, ms: int = 300):
    if screen_sameness(context.refresh(), pos) < same:
        time.sleep(ms / 1000)


@mycmd.command()
def touch_n(context: mycmd.Context, x1: int, y1: int, x2: int, y2: int):
    context.touch(x1, y1, x2, y2)


@mycmd.command()
def touch(context: mycmd.Context, p1: Point, p2: Point):
    context.touch(p1.point().x(), p1.point().y(), p2.point().x(), p2.point().y())


@mycmd.command()
def touch_if(context: mycmd.Context, p1: Point, p2: Point, pos: Rect, same: int = 80):
    if screen_sameness(context['screen'], pos) >= same:
        context.touch(p1.point().x(), p1.point().y(), p2.point().x(), p2.point().y())


@mycmd.command()
def touch_unless(context: mycmd.Context, p1: Point, p2: Point, pos: Rect, same: int = 80):
    if screen_sameness(context['screen'], pos) < same:
        context.touch(p1.point().x(), p1.point().y(), p2.point().x(), p2.point().y())


@mycmd.command()
def click_n(context: mycmd.Context, x: int, y: int):
    context.click(x, y)


@mycmd.command()
def click(context: mycmd.Context, pos: Union[Point, Rect]):
    if isinstance(pos, Point):
        context.click(pos.point().x(), pos.point().y())
    elif isinstance(pos, Rect):
        context.click(pos.rect().center().x(), pos.rect().center().y())


@mycmd.command()
def click_if(context: mycmd.Context, pos: Rect, same: int = 80):
    if screen_sameness(context['screen'], pos) >= same:
        context.click(pos.rect().center().x(), pos.rect().center().y())


@mycmd.command()
def click_unless(context: mycmd.Context, pos: Rect, same: int = 80):
    if screen_sameness(context['screen'], pos) < same:
        context.click(pos.rect().center().x(), pos.rect().center().y())


@mycmd.command()
def click_f(context: mycmd.Context, pos: Rect, same: int = 80):
    maxValue, rect = screen_find(context['screen'], pos)
    if maxValue >= same:
        context.click(rect.center().x(), rect.center().y())


def run(device: Device, values: dict, reader, mainFile, callback=None, loop=True) -> int:
    _screen = None

    def click(x: int, y: int):
        device.click(x, y)

    def touch(x1: int, y1: int, x2: int, y2: int):
        device.touch(x1, y1, x2, y2)

    def refresh():
        nonlocal _screen
        _screen = device.screen()
        return _screen

    commands = {
        'refresh': lambda context: refresh()
    }

    context = mycmd.Context()
    context.click = click
    context.touch = touch
    context['screen'] = lambda: _screen if _screen is not None else refresh()

    def my_callback(file, fragment, result):
        print(file, fragment, result)
        if callback is not None:
            callback(file, fragment, result)

    return mycmd.run(mainFile, reader, context, values=values, commands=commands, exec_callback=my_callback, loop=loop)


def screen_find(screen: QtGui.QImage, pos: Rect) -> Tuple[int, QtCore.QRect]:
    rect = pos.rect()
    image1 = pos.image().copy(rect)
    maxValue, maxLoc = image_find(screen, image1)
    return maxValue, QtCore.QRect(maxLoc[0], maxLoc[1], rect.width(), rect.height())


def screen_sameness(screen: QtGui.QImage, pos: Rect) -> int:
    rect = pos.rect()
    image1 = pos.image().copy(rect)
    image2 = screen.copy(rect)
    return image_sameness(image1, image2)


def image2numpy(image: QtGui.QImage) -> numpy.ndarray:
    arr = numpy.zeros((image.height(), image.width(), 3), dtype=numpy.uint8)
    for x in range(image.width()):
        for y in range(image.height()):
            color = image.pixelColor(x, y)
            arr[y, x, 0] = color.red()
            arr[y, x, 1] = color.green()
            arr[y, x, 2] = color.blue()
    return arr


def image_find(image1: QtGui.QImage, image2: QtGui.QImage) -> Tuple[int, Tuple[int, int]]:
    result = cv2.matchTemplate(image2numpy(image1), image2numpy(image2), cv2.TM_CCOEFF_NORMED)
    _, maxValue, _, maxLoc = cv2.minMaxLoc(result)
    return int(maxValue * 100), maxLoc


def image_sameness(image1: QtGui.QImage, image2: QtGui.QImage) -> int:
    a = image2numpy(image1)
    b = image2numpy(image2)
    return int(numpy.sum(a == b) / a.size * 100)
