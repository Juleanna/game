@echo off
title TimeZero Game Server

echo ===============================================================
echo   TimeZero - Post-apocalyptic MMORPG
echo ===============================================================
echo.

:: Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Install Python 3.11+ and try again.
    pause
    exit /b 1
)

:: Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found! Install Node.js and try again.
    pause
    exit /b 1
)

echo OK: Python found
python --version
echo OK: Node.js found
node --version
echo.

:: Check backend venv
if not exist "backend\venv" (
    echo Creating virtual environment for backend...
    cd backend
    python -m venv venv
    cd ..
    echo OK: Virtual environment created
    echo.
)

:: Check backend dependencies
if not exist "backend\venv\Lib\site-packages\fastapi" (
    echo Installing backend dependencies...
    cd backend
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
    echo OK: Backend dependencies installed
    echo.
)

:: Check frontend dependencies
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
    echo OK: Frontend dependencies installed
    echo.
)

:: Check database
if not exist "database\timezero.db" (
    echo Database not found. Running seed script...
    cd backend
    call venv\Scripts\activate.bat
    python seed_data.py
    cd ..
    echo OK: Database populated
    echo.
) else (
    echo OK: Database found
    echo.
)

echo ===============================================================
echo   Starting servers...
echo ===============================================================
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:5173
echo API documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop servers
echo.

:: Start backend in new window
start "TimeZero Backend" cmd /k "cd backend && venv\Scripts\activate.bat && echo Starting Backend server... && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

:: Wait for backend to start
timeout /t 3 /nobreak > nul

:: Start frontend in new window
start "TimeZero Frontend" cmd /k "cd frontend && echo Starting Frontend server... && npm run dev"

echo.
echo ===============================================================
echo   Servers started!
echo ===============================================================
echo.
echo Open your browser and go to http://localhost:5173
echo.
echo Useful commands:
echo    - Register: create new account
echo    - Create character: choose one of 14 professions
echo    - Start game in New Moscow!
echo.
echo Enjoy the game!
echo.
pause
