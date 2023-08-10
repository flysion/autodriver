import subprocess

from PySide6 import QtGui


class ADB:
    def __init__(self, name=None):
        super(ADB, self).__init__()
        self._name = name
        self._shell = subprocess.Popen(self.command('shell'), text=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    def command(self, *args):
        if self._name is not None:
            return ['adb', '-s', self._name, *[str(arg) for arg in args]]
        else:
            return ['adb', *args]

    def shell(self, *args):
        print(' '.join([str(arg) for arg in args]) + "\n")
        self._shell.stdin.write(' '.join([str(arg) for arg in args]) + "\n")
        self._shell.stdin.flush()

    def input(self, text):
        self.shell('input', 'text', text)

    def click(self, x, y):
        self.shell('input', 'tap', x, y)

    def dbclick(self, x, y):
        self.shell('input', 'tap', x, y, '&', 'input', 'tap', x, y)

    def touch(self, x1, y1, x2, y2):
        self.shell('input', 'swipe', x1, y1, x2, y2)

    def screen(self) -> QtGui.QImage:
        p = subprocess.run(self.command('exec-out', 'screencap', '-p'), capture_output=True, shell=False, check=False)
        return QtGui.QImage.fromData(p.stdout)

    def exit(self):
        self.shell('exit')
        self._shell.kill()
