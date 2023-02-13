import subprocess

from PySide6 import QtGui


class Device:
    def click(self, x, y):
        pass

    def move(self, x1, y1, x2, y2):
        pass

    def screen(self) -> QtGui.QImage:
        pass


class ADBException(BaseException):
    def __init__(self, message):
        self._message = message


class ADB(Device):
    def __init__(self, name=None):
        super(ADB, self).__init__()
        self._name = name

    def build_command(self, *args):
        command = ['adb']
        if self._name is not None:
            command.append('-s')
            command.append(self._name)

        return command + list(args)

    def click(self, x, y):
        code, out = subprocess.getstatusoutput(self.build_command('shell', 'input', 'tap', str(x), str(y)))
        if code != 0:
            raise ADBException(out)

    def move(self, x1, y1, x2, y2):
        code, out = subprocess.getstatusoutput(self.build_command('shell', 'input', 'swipe', str(x1), str(y1), str(x2), str(y2)))
        if code != 0:
            raise ADBException(out)

    def screen(self) -> QtGui.QImage:
        p = subprocess.run(self.build_command('shell', 'screencap', '-p'), capture_output=True, shell=True, check=False)
        if p.returncode != 0:
            raise ADBException(p.stderr.decode('utf8'))
        return QtGui.QImage.fromData(p.stdout.replace(b'\r\n', b'\n'))
