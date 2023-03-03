from typing import Union, Tuple

import cv2
import numpy
from PySide6 import QtGui, QtCore

import myexecutor
from Device import Device


class Point:
    def __init__(self, image: QtGui.QImage, point: QtCore.QPoint):
        self._image = image
        self._point = point

    def x(self):
        return self._point.x()

    def y(self):
        return self._point.y()

    def image(self):
        return self._image

    def point(self):
        return self._point


class Rect:
    def __init__(self, image: QtGui.QImage, rect: QtCore.QRect):
        self._image = image
        self._rect = rect

    def x(self):
        return self._rect.center().x()

    def y(self):
        return self._rect.center().y()

    def image(self):
        return self._image

    def rect(self):
        return self._rect


@myexecutor.command()
def run_if(context: myexecutor.Context, pos: Rect, file, same: int = 80):
    if screen_sameness(context.screen(), pos) >= same:
        context.run(file)


@myexecutor.command()
def run_unless(context: myexecutor.Context, pos: Rect, file, same: int = 80):
    if screen_sameness(context.screen(), pos) < same:
        context.run(file)


@myexecutor.command()
def exit_if(context: myexecutor.Context, pos: Rect, code: int = 0, same: int = 80):
    if screen_sameness(context.screen(), pos) >= same:
        context.exit(code)


@myexecutor.command()
def exit_unless(context: myexecutor.Context, pos: Rect, code: int = 0, same: int = 80):
    if screen_sameness(context.screen(), pos) < same:
        context.exit(code)


@myexecutor.command()
def goto_if(context: myexecutor.Context, pos: Rect, label: myexecutor.Label, same: int = 80):
    if screen_sameness(context.screen(), pos) >= same:
        context.goto(label)


@myexecutor.command()
def goto_unless(context: myexecutor.Context, pos: Rect, label: myexecutor.Label, same: int = 80):
    if screen_sameness(context.screen(), pos) < same:
        context.goto(label)


@myexecutor.command()
def wait(context: myexecutor.Context, ms: int):
    context.sleep(ms / 1000)


@myexecutor.command()
def wait_if(context: myexecutor.Context, pos: Rect, ms: int, same: int = 80):
    if screen_sameness(context.screen(), pos) >= same:
        context.sleep(ms / 1000)


@myexecutor.command()
def wait_unless(context: myexecutor.Context, pos: Rect, ms: int, same: int = 80):
    if screen_sameness(context.screen(), pos) < same:
        context.sleep(ms / 1000)


@myexecutor.command()
def refresh_till(context: myexecutor.Context, pos: Rect, ms: int = 300, same: int = 80):
    if screen_sameness(context.refresh(), pos) >= same:
        context.sleep(ms / 1000)


@myexecutor.command()
def refresh_till_not(context: myexecutor.Context, pos: Rect, ms: int = 300, same: int = 80):
    if screen_sameness(context.refresh(), pos) < same:
        context.sleep(ms / 1000)


@myexecutor.command()
def touch_n(context: myexecutor.Context, x1: int, y1: int, x2: int, y2: int):
    context.touch(x1, y1, x2, y2)


@myexecutor.command()
def touch(context: myexecutor.Context, p1: Point, p2: Point):
    context.touch(p1.point().x(), p1.point().y(), p2.point().x(), p2.point().y())


@myexecutor.command()
def touch_if(context: myexecutor.Context, p1: Point, p2: Point, pos: Rect, same: int = 80):
    if screen_sameness(context.screen(), pos) >= same:
        context.touch(p1.point().x(), p1.point().y(), p2.point().x(), p2.point().y())


@myexecutor.command()
def touch_unless(context: myexecutor.Context, p1: Point, p2: Point, pos: Rect, same: int = 80):
    if screen_sameness(context.screen(), pos) < same:
        context.touch(p1.point().x(), p1.point().y(), p2.point().x(), p2.point().y())


@myexecutor.command()
def click_n(context: myexecutor.Context, x: int, y: int):
    context.click(x, y)


@myexecutor.command()
def click(context: myexecutor.Context, pos: Union[Point, Rect]):
    context.click(pos.x(), pos.y())


@myexecutor.command()
def click_if(context: myexecutor.Context, pos: Rect, same: int = 80):
    if screen_sameness(context.screen(), pos) >= same:
        context.click(pos.x(), pos.y())


@myexecutor.command()
def click_unless(context: myexecutor.Context, pos: Rect, same: int = 80):
    if screen_sameness(context.screen(), pos) < same:
        context.click(pos.x(), pos.y())


@myexecutor.command()
def click_find(context: myexecutor.Context, pos: Rect, click_pos: Union[Point, Rect] = None, same: int = 80):
    maxValue, rect = screen_find(context.screen(), pos)
    if maxValue >= same:
        if click_pos is None:
            context.click(rect.center().x(), rect.center().y())
        else:
            context.click(click_pos.x(), click_pos.y())


@myexecutor.command()
def input(context: myexecutor.Context, text: str):
    context.input(text)


def exec(device: Device, variables: dict, reader, main, refresh_callback=None, click_callback=None, touch_callback=None, print_fn=print, **kwargs) -> int:
    _screen = None

    def click(x: int, y: int):
        device.click(x, y)
        if click_callback is not None:
            click_callback(x, y)

    def touch(x1: int, y1: int, x2: int, y2: int):
        device.touch(x1, y1, x2, y2)
        if touch_callback is not None:
            touch_callback(x1, y1, x2, y2)

    def refresh():
        nonlocal _screen
        _screen = device.screen()
        if refresh_callback is not None:
            refresh_callback(_screen)
        return _screen

    context = myexecutor.Context(items=variables)
    context.input = device.input
    context.click = click
    context.touch = touch
    context.screen = lambda: _screen if _screen is not None else refresh()
    context.print = print_fn

    # 满足以下条件在此注册 commands：context中无法访问的方法需要暴露到用户侧的
    commands = {
        'refresh': lambda context: refresh(),
        'print': lambda context, text: print_fn(text),
    }

    return myexecutor.exec(main, reader, context, commands=commands, **kwargs)


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


if __name__ == '__main__':
    # TODO 执行DDI文件，编译成命令行程序
    pass
