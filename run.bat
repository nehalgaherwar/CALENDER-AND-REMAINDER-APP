@echo off
REM Calendar and Reminder App - Setup and Launch Script for Windows

echo.
echo ============================================================
echo    Calendar and Reminder App - Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=*" %%i in ('python --version') do (
    echo Found: %%i
)
echo.

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Warning: Some dependencies may have failed to install
    echo Attempting minimal installation...
    pip install customtkinter pillow tkcalendar playsound
)

echo.
echo Setup complete!
echo Launching Calendar and Reminder App...
echo.

REM Launch the application
python main.py

pause
