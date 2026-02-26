@echo off
REM ================================================
REM Grimlock Portable Starter - Windows Batch File
REM ================================================

REM -- Step 1: Bootstrap environment (install dependencies, create folders/config)
echo [*] Running bootstrap.py...
python bootstrap.py
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Error during bootstrap. Exiting.
    pause
    exit /b %ERRORLEVEL%
)

REM -- Step 2: Run Grimlock Portable
echo [*] Launching Grimlock Portable...
python desktop.py
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Error during launch. Exiting.
    pause
    exit /b %ERRORLEVEL%
)

REM -- Step 3: Finished
echo [*] Grimlock Portable should now be running!
pause