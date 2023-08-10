import time
from typing import Mapping, Callable

from .context import Context
from .yacc import parse

_global_commands = {}


class CommandNotFound(Exception):
    def __init__(self, file, fragment):
        self.file = file
        self.fragment = fragment


class VariableNotFound(Exception):
    def __init__(self, file, arg):
        self.file = file
        self.arg = arg


class LabelNotFound(Exception):
    def __init__(self, file, name):
        self.file = file
        self.name = name


class Label:
    def __init__(self, index, fragment):
        self._index = index
        self._fragment = fragment

    def index(self):
        return self._index

    def fragment(self):
        return self._fragment


def exec(main, reader, context: Context, commands: Mapping[str, Callable] = {},
         loop=True, quit: Callable = None, pause: Callable = None, sleep: Callable = None,
         exec_callback: Callable = None) -> int:
    _exitcode: int = None
    _quit: bool = False

    def exit(code: int = 0):
        nonlocal _exitcode
        _exitcode = code

    def read(file):
        return parse(str(reader(file)))

    def is_quit():
        nonlocal _quit
        if not _quit and quit is not None:
            _quit = quit()
        return _quit

    context.exit = exit
    context.sleep = lambda second: sleep(second) if sleep is not None else time.sleep(second)

    def run(file):
        _fragments: list = read(file)
        _index: int = 0
        _labels = {}

        if pause is not None:
            while pause():
                sleep(100)

        for index in range(len(_fragments)):
            fragment = _fragments[index]
            if fragment['type'] == 'label':
                _labels[fragment['name']] = Label(index, fragment)

        def goto(label: Label):
            nonlocal _index
            _index = label.index()

        def variable(option):
            if option['type'] == 'keyword':
                variables = {**context.items(), **_labels}
                key = option['text']
                if key not in variables:
                    raise VariableNotFound(file, option)
                value = variables[key]
                if callable(value):
                    return value()
                else:
                    return value
            elif option['type'] == 'string':
                return option['text']
            elif option['type'] == 'integer':
                return int(option['text'])
            elif option['type'] == 'float':
                return float(option['text'])
            elif option['type'] == 'bool':
                return option['text'].lower() == 'true'
            elif option['type'] == 'null':
                return None
            else:
                pass

        context.run = run
        context.goto = goto

        _commands = dict(commands, **_global_commands, **{
            'run': lambda context, file: run(file),
            'goto': lambda context, label: goto(label),
            'exit': lambda context, code=0: exit(code),
        })

        def exec_command(name, args, kwargs):
            if name not in _commands:
                raise CommandNotFound(file, fragment)

            fn = _commands[name]

            _args = [context]
            for arg in args:
                _args.append(variable(arg))

            _kwargs = {}
            for kwarg in kwargs:
                _kwargs[kwarg['name']] = variable(kwarg['value'])

            return fn(*_args, **_kwargs)

        while _exitcode is None and not is_quit():
            if _index >= len(_fragments):
                break

            fragment = _fragments[_index]

            if fragment['type'] == 'command':
                result = exec_command(fragment['name'], fragment['args'], fragment['kwargs'])
            elif fragment['type'] == 'label':
                continue
            else:
                result = None

            _index += 1

            if exec_callback is not None:
                exec_callback(context, file, fragment, result)

    while not is_quit():
        run(main)
        if _exitcode is not None or not loop:
            break

    return _exitcode if _exitcode is not None else 0


def command(name=None):
    def decorator(fn):
        global _global_commands
        key = fn.__name__ if name is None else name
        _global_commands[key] = fn
        return fn

    return decorator
