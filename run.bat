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
    echo Install Python 3.10+ and make sure python is available in PATH.
    pause
    exit /b 1
)

if exist "requirement.txt" (
    echo Installing dependencies from requirement.txt...
    "%PYTHON_CMD%" -m pip install -r requirement.txt
    if errorlevel 1 (
        echo Dependency install failed.
        pause
        exit /b 1
    )
)

:menu
cls
echo ================================
echo Poetry Agent Launcher
echo ================================
echo 1. Start Streamlit app
echo 2. Start FastAPI server
echo 3. Exit
set /p choice="Select an option [1-3]: "

if "%choice%"=="1" goto app
if "%choice%"=="2" goto server
if "%choice%"=="3" exit /b 0

echo Invalid option.
pause
goto menu

:app
cls
echo Starting Poetry AI Streamlit app...
"%PYTHON_CMD%" -m streamlit run streamlit_app.py
if errorlevel 1 (
    echo The app exited with an error.
    pause
)
exit /b 0

:server
cls
echo Starting Poetry AI FastAPI server...
"%PYTHON_CMD%" server.py
if errorlevel 1 (
    echo The server exited with an error.
    pause
)
exit /b 0
