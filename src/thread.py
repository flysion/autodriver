from PySide6 import QtCore

_threads = {}


class Thread(QtCore.QThread):
    def __init__(self, fn, *args, **kwargs):
        super(Thread, self).__init__()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def run(self) -> None:
        self._fn(*self._args, **self._kwargs)


def on_thread_finished(thread: Thread):
    global _threads
    del _threads[id(thread)]


def async_(fn, *args, **kwargs):
    global _threads
    thread = Thread(fn, *args, **kwargs)
    thread.finished.connect(lambda thread=thread: on_thread_finished(thread))
    _threads[id(thread)] = thread
    thread.start()
