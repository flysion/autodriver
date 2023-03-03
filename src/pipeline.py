from functools import reduce
from typing import Callable


class Pipeline:
    class Carry:
        def __init__(self, stack, pipe):
            self._stack = stack
            self._pipe = pipe

        def __call__(self, *args, **kwargs):
            if self._pipe is None:
                return self._stack(*args, **kwargs)
            return self._pipe(self._stack, *args, **kwargs)

    class Destination:
        def __init__(self, destination: Callable):
            self._destination = destination

        def __call__(self, *args, **kwargs):
            if self._destination is None:
                return
            return self._destination(*args, **kwargs)

    def __init__(self):
        self._pipes = []
        self._destination = None

    def through(self, *pipes: Callable):
        self._pipes.extend(pipes)
        return self

    def then(self, destination: Callable):
        self._destination = destination
        return self

    def destination(self) -> Callable:
        return Pipeline.Destination(self._destination)

    def carry(self) -> Callable:
        return lambda pipe, stack: Pipeline.Carry(pipe, stack)

    def __call__(self, *args, **kwargs):
        return reduce(self.carry(), self._pipes[::-1], self.destination())(*args, **kwargs)


class Stack(Pipeline):
    class Carry:
        def __init__(self, stack, pipe):
            self._stack = stack
            self._pipe = pipe

        def __call__(self, *args, **kwargs):
            if self._pipe is not None:
                self._pipe(*args, **kwargs)
            return self._stack(*args, **kwargs)

    def carry(self) -> Callable:
        return lambda pipe, stack: Stack.Carry(pipe, stack)
