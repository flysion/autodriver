from typing import Mapping, Callable

from .context import Context
from .yacc import parser

_global_commands = {}


class CommandNotFound(Exception):
    def __init__(self, file, line):
        self.file = file
        self.line = line


class ValueNotFound(Exception):
    def __init__(self, file, arg):
        self.file = file
        self.arg = arg


def run(reader, mainFile, context: Context = None, values: dict = {}, commands: Mapping[str, Callable] = {}, exec_callback=None, loop=True) -> int:
    _exitcode: int = None
    _parse_cache: dict = {}

    def exit(exitcode: int = 0):
        nonlocal _exitcode
        _exitcode = exitcode

    def readFile(file):
        nonlocal _parse_cache
        fileid = id(file)
        if fileid not in _parse_cache:
            _parse_cache[fileid] = parser.parse(str(reader(file)))
        return _parse_cache[fileid]

    def runFile(file):
        _file_object: list = readFile(file)
        _index: int = 0
        _labels = {}

        for index in range(len(_file_object)):
            item = _file_object[index]
            if item['type'] == 'label':
                _labels[item['name']] = (index, item)

        _values = {**_labels, **values}

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

        context.load = runFile
        context.goto = goto
        context.exit = exit

        _commands = dict(commands, **_global_commands, **{
            'load': lambda context, file: runFile(file),
            'goto': lambda context, label: goto(label),
            'exit': lambda context, exitcode: exit(exitcode),
        })

        while _exitcode is None:
            if _index >= len(_file_object):
                break

            item = _file_object[_index]

            if item['type'] == 'command':  # 指令
                name = item['name']
                if name not in _commands:
                    raise CommandNotFound(file, item)
                fn = _commands[name]

                args = [context]
                for arg in item['args']:
                    args.append(value(arg))

                kwargs = {}
                for kwarg in item['kwargs']:
                    kwargs[kwarg['name']] = value(kwarg['value'])

                result = fn(*args, **kwargs)
            else:
                result = None

            _index += 1

            if exec_callback is not None:
                exec_callback(file, item, result)

    while True:
        runFile(mainFile)
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
