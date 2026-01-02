@echo off
REM run_tests.bat - Test runner script for the fuzzbench project
REM Works from a clean checkout and manages an isolated virtual environment

setlocal enabledelayedexpansion
set VENV_DIR=.venv

echo.
echo ================================
echo Checking Python installation
echo ================================

python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.10+ and ensure it's in PATH.
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found: %PYTHON_VERSION%

echo.
echo ================================
echo Setting up virtual environment
echo ================================

if exist %VENV_DIR% (
    echo Virtual environment exists at %VENV_DIR%
) else (
    echo Creating new virtual environment at %VENV_DIR%...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        exit /b 1
    )
)

echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    exit /b 1
)

echo.
echo ================================
echo Upgrading pip
echo ================================

python -m pip install --upgrade pip setuptools wheel >nul 2>&1
if errorlevel 1 (
    echo Error: Failed to upgrade pip
    exit /b 1
)

echo.
echo ================================
echo Installing dependencies
echo ================================

if exist requirements.txt (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        exit /b 1
    )
) else (
    echo Error: requirements.txt not found
    exit /b 1
)

echo.
echo ================================
echo Installing package in editable mode
echo ================================

pip install -e .
if errorlevel 1 (
    echo Error: Failed to install package
    exit /b 1
)

echo.
echo ================================
echo Running test suite
echo ================================

pytest -v
if errorlevel 1 (
    echo Error: Tests failed
    exit /b 1
)

echo.
echo ================================
echo Test run completed successfully
echo ================================

endlocal
