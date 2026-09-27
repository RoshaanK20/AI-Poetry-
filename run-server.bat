@echo off
cd /d "%~dp0"

set "PYTHON_CMD=python"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_CMD=.venv\Scripts\python.exe"
) else if exist "venv\Scripts\python.exe" (
    set "PYTHON_CMD=venv\Scripts\python.exe"
)

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found in PATH.
    echo Please install Python 3.10+ and make sure it is available in PATH.
    pause
    exit /b 1
)

if exist "requirement.txt" (
    echo Installing Python dependencies...
    "%PYTHON_CMD%" -m pip install -r requirement.txt
    if errorlevel 1 (
        echo Dependency install failed.
        pause
        exit /b 1
    )
)

echo Starting Poetry API server...
"%PYTHON_CMD%" server.py

if errorlevel 1 (
    echo The server exited with an error.
    pause
)
