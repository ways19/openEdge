@echo off
REM Pastikan sudah install pyinstaller: pip install pyinstaller
pyinstaller --onefile --windowed --icon=app.ico openEdge.spec
pause