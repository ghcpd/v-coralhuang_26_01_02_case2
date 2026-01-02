@echo off
setlocal enabledelayedexpansion

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment.
        exit /b 1
    )
)

REM Activate virtual environment
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment.
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    exit /b 1
)

REM Install the package in editable mode
echo Installing package...
pip install -e .
if %errorlevel% neq 0 (
    echo ERROR: Failed to install package.
    exit /b 1
)

REM Run tests
echo Running tests...
pytest
if %errorlevel% neq 0 (
    echo ERROR: Tests failed.
    exit /b 1
)

echo All tests passed!