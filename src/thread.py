from PySide6 import QtCore


class Async(QtCore.QThread):
    def __init__(self, fn, *args, **kwargs):
        super(Async, self).__init__()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def run(self) -> None:
        self._fn(*self._args, **self._kwargs)


class Tick(QtCore.QThread):
    def __init__(self, fn, ms, total, *args, **kwargs):
        super(Tick, self).__init__()
        self._ms = ms
        self._total = total
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def run(self) -> None:
        for i in range(self._total):
            self._fn(*self._args, **self._kwargs)
            self.msleep(self._ms)
