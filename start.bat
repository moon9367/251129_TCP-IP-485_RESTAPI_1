@echo off
chcp 65001 >nul 2>&1
title Sensor Collector
color 0B

REM Change to script directory
cd /d "%~dp0"
echo Current directory: %CD%

echo.
echo ================================================================================
echo Smart Farm - Sensor Data Collector
echo ================================================================================
echo.
echo This script collects Modbus sensor values periodically.
echo.
echo Collection interval: 10 seconds
echo Collection items: Temperature, Humidity, Solar Radiation, etc.
echo.
echo Press Ctrl+C to stop.
echo.
pause

REM ============================================================================
REM Python Environment Check
REM ============================================================================
echo.
echo ================================================================================
echo Python Environment Check
echo ================================================================================

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo No virtual environment. Using system Python.
)

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed!
    echo Download Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python installation confirmed

REM Check required packages
echo Checking required packages...
python -c "import pymodbus" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Required packages not installed!
    echo Installing packages...
    echo.
    pip install pymodbus
    if errorlevel 1 (
        echo.
        echo ERROR: Package installation failed!
        echo.
        echo Manual installation:
        echo    pip install pymodbus
        echo.
        pause
        exit /b 1
    )
    echo Package installation completed
) else (
    echo Required packages confirmed
)

REM ============================================================================
REM Run Sensor Collection Script
REM ============================================================================
echo.
echo ================================================================================
echo Starting Sensor Data Collection
echo ================================================================================
echo.

REM Run Python script with absolute path
python "%~dp0sensor_collector.py"

echo.
echo ================================================================================
echo Sensor Data Collection Stopped
echo ================================================================================
echo.
pause

