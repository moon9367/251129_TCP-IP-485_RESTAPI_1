@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ======================================================================
echo Smart Farm Sensor Data Collector
echo ======================================================================
echo.

REM Python check
echo [1/3] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo         Please install Python 3.7 or higher
    echo         Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python --version
echo.

REM Package check
echo [2/3] Checking required packages...
python -c "import pymodbus" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] pymodbus package not found
    echo           Installing automatically...
    echo.
    pip install pymodbus>=3.0.0
    if %errorlevel% neq 0 (
        echo [ERROR] Package installation failed. Check internet connection.
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] pymodbus installed
) else (
    echo [OK] pymodbus package found
)
echo.

REM File check
echo [3/3] Checking required files...
if not exist "temp_sensor_collector.py" (
    echo [ERROR] temp_sensor_collector.py not found
    echo.
    pause
    exit /b 1
)
if not exist "modbus_tcp_controller.py" (
    echo [ERROR] modbus_tcp_controller.py not found
    echo.
    pause
    exit /b 1
)
if not exist "control_specs.py" (
    echo [ERROR] control_specs.py not found
    echo.
    pause
    exit /b 1
)
echo [OK] All required files found
echo.

echo ======================================================================
echo Starting program...
echo ======================================================================
echo.

python temp_sensor_collector.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Program exited with error code: %errorlevel%
)

echo.
pause
