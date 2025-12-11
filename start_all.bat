@echo off
chcp 65001 >nul
title Smart Farm - REST API + Cloudflare Tunnel
color 0A

echo.
echo ================================================================================
echo Smart Farm - REST API + Cloudflare Tunnel
echo ================================================================================
echo.
echo This script will automatically run:
echo    1. REST API Server (Python FastAPI)
echo    2. Cloudflare Tunnel (HTTPS External Access)
echo.
echo Two windows will open. Keep both running!
echo.
echo To exit: Press Ctrl + C in each window or close the windows
echo.
pause

REM ============================================================================
REM Step 1: Check Python Environment
REM ============================================================================
echo.
echo ================================================================================
echo Step 1: Check Python Environment
echo ================================================================================

REM Activate Python virtual environment (if exists)
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo No virtual environment found. Using system Python.
)

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed!
    echo Please download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python installation confirmed

REM Check required packages
echo Checking required packages...
python -c "import fastapi, uvicorn, pymodbus" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Required packages not installed!
    echo Installing packages...
    echo.
    
    REM Install packages individually to avoid encoding issues
    pip install fastapi==0.104.1
    pip install uvicorn[standard]==0.24.0
    pip install pymodbus==3.5.4
    pip install pydantic==2.5.0
    pip install python-multipart==0.0.6
    pip install requests==2.31.0
    pip install xmltodict==0.13.0
    
    if errorlevel 1 (
        echo.
        echo ERROR: Package installation failed!
        echo.
        echo Please install manually:
        echo    pip install fastapi uvicorn[standard] pymodbus pydantic python-multipart requests xmltodict
        echo.
        pause
        exit /b 1
    )
    echo Package installation complete
) else (
    echo Required packages confirmed
)

REM ============================================================================
REM Step 2: Check Cloudflared
REM ============================================================================
echo.
echo ================================================================================
echo Step 2: Check Cloudflared
echo ================================================================================

where cloudflared >nul 2>&1
if errorlevel 1 (
    echo WARNING: cloudflared not installed!
    echo.
    echo Installation options:
    echo.
    echo [Option 1] Download Cloudflared (Recommended)
    echo    1. Visit: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
    echo    2. Download Windows version
    echo    3. Copy cloudflared.exe to this folder
    echo.
    echo [Option 2] Use NPX (Requires Node.js)
    echo    npx cloudflared tunnel --url http://localhost:8000
    echo.
    echo [Option 3] Use Winget (Windows 11)
    echo    winget install --id Cloudflare.cloudflared
    echo.
    set /p continue="Do you want to run REST API only without Tunnel? (Y/N): "
    if /i "%continue%"=="Y" goto :skip_tunnel
    pause
    exit /b 1
) else (
    echo Cloudflared installation confirmed
)

REM ============================================================================
REM Step 3: Start REST API Server (Separate Window)
REM ============================================================================
:skip_tunnel
echo.
echo ================================================================================
echo Step 3: Start REST API Server
echo ================================================================================
echo.
echo Starting REST API Server in new window...

REM Start REST API Server in new window
start "REST API Server" cmd /k "title REST API Server && color 0B && python rest_api_server.py"

REM Wait for server to start (5 seconds)
echo Waiting for REST API Server to start... (5 seconds)
timeout /t 5 /nobreak >nul

REM Test server connection
echo Testing REST API Server connection...
curl http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo WARNING: REST API Server connection failed!
    echo Please check the REST API Server window.
    set /p continue="Continue anyway? (Y/N): "
    if /i not "%continue%"=="Y" exit /b 1
) else (
    echo REST API Server connection successful!
    echo API Documentation: http://localhost:8000/docs
)

REM If cloudflared not installed, end here
where cloudflared >nul 2>&1
if errorlevel 1 goto :end_without_tunnel

REM ============================================================================
REM Step 4: Start Cloudflare Tunnel (Current Window)
REM ============================================================================
echo.
echo ================================================================================
echo Step 4: Start Cloudflare Tunnel
echo ================================================================================
echo.
echo Cloudflare Tunnel URL will be displayed below:
echo    https://xxxx-xxxx-xxxx.trycloudflare.com
echo.
echo Copy this URL and enter it in web_ui/api-config.js BASE_URL!
echo.
echo Required for Netlify deployment!
echo.
echo To exit: Press Ctrl + C
echo.
echo ================================================================================
echo.

REM Start Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8000

REM When tunnel is closed
goto :end

REM ============================================================================
REM End without Cloudflared
REM ============================================================================
:end_without_tunnel
echo.
echo ================================================================================
echo REST API Server Only (Running)
echo ================================================================================
echo.
echo Local Access: http://localhost:8000/docs
echo.
echo To use Cloudflare Tunnel:
echo    1. Install cloudflared
echo    2. Run this script again
echo.
echo To exit: Press any key (REST API Server will continue in separate window)
echo.
pause
goto :end

REM ============================================================================
REM End
REM ============================================================================
:end
echo.
echo ================================================================================
echo Cloudflare Tunnel Closed
echo ================================================================================
echo.
echo WARNING: REST API Server is still running in separate window.
echo To close REST API Server, close that window.
echo.
pause
