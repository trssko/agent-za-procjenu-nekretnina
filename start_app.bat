@echo off
echo ===========================================
echo   Housing Valuation Agent - Startup Script
echo ===========================================

echo.
echo [1/2] Starting Backend Server (FastAPI)...
start "Backend Agent" cmd /k "py -m uvicorn web.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo [2/2] Starting Frontend Server (React)...
cd frontend
start "Frontend UI" cmd /k "npm run dev"

echo.
echo ===========================================
echo   System is running!
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo ===========================================
echo.
pause
