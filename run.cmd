@echo off
setlocal enabledelayedexpansion
cd %~dp0

rem List of required Python libraries
set "libs=flask psutil humanize py-cpuinfo gputil"
set "libspre=flask psutil humanize cpuinfo gputil"

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python first.
    exit /b 1
)

rem Check and install required Python libraries
for %%i in (%libspre%) do (
    python -c "import %%i" 2>nul
    if !errorlevel! neq 0 (
        echo Installing %%i...
        pip install %%i
        if !errorlevel! neq 0 (
            echo Failed to install %%i. Please check your internet connection and try again.
            exit /b 1
        )
    ) else (
        echo %%i is already installed. Skipping...
    )
)

cls
echo ===========================================
echo running server...
echo ===========================================
python app.py
exit /b 0
