@echo off
echo Starting DoroLexus Vocabulary Flashcard App...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if PySide6 is installed
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo Installing PySide6...
    pip install PySide6
    if errorlevel 1 (
        echo Error: Failed to install PySide6
        pause
        exit /b 1
    )
)

REM Run the application
python main.py

pause
