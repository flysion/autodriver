@echo off

set DIR=%~dp0
cd %DIR%

rd /q /s "build"
rd /q /s "dist"

pyinstaller -n "autodriver" --distpath=dist --workpath=build -F -D -w src/main.py

pause