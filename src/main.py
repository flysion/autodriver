# coding: utf-8
# pyqt docs: https://doc.qt.io/qtforpython-6/

if __name__ == '__main__':
    import logging
    import sys
    from MainWindow import MainWindow
    from PySide6.QtWidgets import QApplication
    from device import ADB
    import os

    app = QApplication([])
    adb = ADB()

    w = MainWindow(adb, file=os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else None)
    w.show()

    try:
        sys.exit(app.exec())
    except Exception as e:
        logging.error('应用程序错误：{e}'.format(e=repr(e)))
    finally:
        adb.exit()
