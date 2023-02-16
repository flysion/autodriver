from typing import Mapping, Callable

from .context import Context
from .yacc import parser

_global_commands = {}


class CommandNotFound(Exception):
    def __init__(self, file, fragment):
        self.file = file
        self.fragment = fragment


class ValueNotFound(Exception):
    def __init__(self, file, arg):
        self.file = file
        self.arg = arg


def run(mainFile, reader, context: Context, values: dict = {}, commands: Mapping[str, Callable] = {}, exec_callback=None, loop=True) -> int:
    _exitcode: int = None
    _cache: dict = {}

    def exit(exitcode: int = 0):
        nonlocal _exitcode
        _exitcode = exitcode

    def read(file):
        nonlocal _cache
        key = id(file)
        if key not in _cache:
            _cache[key] = parser.parse(str(reader(file)))
        return _cache[key]

    def runFile(file):
        _fragments: list = read(file)
        _index: int = 0
        _labels = {}
        _values = {}  # TODO

        for index in range(len(_fragments)):
            fragment = _fragments[index]
            if fragment['type'] == 'label':
                _labels[fragment['name']] = (index, fragment)

        _values = {**values, **_values, **_labels}

        def goto(label):
            nonlocal _index
            _index = label[0]

        def value(option):
            if option['type'] == 'keyword':
                key = option['text']
                if key not in _values:
                    raise ValueNotFound(file, option)
                val = _values[key]
                if callable(val):
                    return val()
                else:
                    return val
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

        context.run = runFile
        context.goto = goto
        context.exit = exit

        _commands = dict(commands, **_global_commands, **{
            'run': lambda context, file: runFile(file),
            'goto': lambda context, label: goto(label),
            'exit': lambda context, exitcode: exit(exitcode),
        })

        while _exitcode is None:
            if _index >= len(_fragments):
                break

            fragment = _fragments[_index]

            if fragment['type'] == 'command':  # 指令
                name = fragment['name']
                if name not in _commands:
                    raise CommandNotFound(file, fragment)
                fn = _commands[name]

                args = [context]
                for arg in fragment['args']:
                    args.append(value(arg))

                kwargs = {}
                for kwarg in fragment['kwargs']:
                    kwargs[kwarg['name']] = value(kwarg['value'])

                result = fn(*args, **kwargs)
            else:
                result = None

            _index += 1

            if exec_callback is not None:
                exec_callback(file, fragment, result)

    while True:
        load(mainFile)
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


@command("print")
def myprint(context: Context, s: str):
    print(s)
