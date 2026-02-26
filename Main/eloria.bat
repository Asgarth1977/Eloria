@echo off
REM ===============================================
REM Eloria Local AI Assistant Launcher
REM ===============================================

REM Set Python executable path
set PYTHON_EXE=C:\Users\mbaeg\AppData\Local\Microsoft\WindowsApps\python3.13.exe

REM Set working directory where eloria.py is located
set WORKDIR=F:\Local AI\Eloria

REM Navigate to working directory
cd /d "%WORKDIR%"

echo Starting Eloria Local AI Assistant...
echo.

REM Run Python script
"%PYTHON_EXE%" app.py

echo.
echo Eloria has exited. Press any key to close this window.
pause