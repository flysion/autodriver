@echo off

set DIR=%~dp0
cd %DIR%

pyside6-uic ui/MainWindow.ui -o src/ui/MainWindow.py

rem pyside6-rcc resources/resources.qrc -o src/resources_rc.py

python src/main.py test.ddi

pause