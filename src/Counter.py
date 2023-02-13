class Counter:
    def __init__(self, start=0, step=1):
        self._start = start
        self._step = step

    def start(self) -> int:
        return self._start

    def step(self) -> int:
        return self._step

    def next(self):
        self._start += self._step
        return self._start
