@echo off
echo ?? LRLRE ENTERPRISE GRID - LAUNCHER
echo ===================================
echo.

REM Kill any existing processes
echo Stopping any existing services...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8007') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8009') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8013') do taskkill /F /PID %%a 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting all services...
echo.

REM Launch each version in a new window
start "LRLRE v7.0 Analysis" cmd /k "cd /d %~dp0 && python start_analytics_v7.py"
timeout /t 2 /nobreak >nul

start "LRLRE v8.2 Visual" cmd /k "cd /d %~dp0 && python start_analytics_v8_bento_grid.py"
timeout /t 2 /nobreak >nul

start "LRLRE v10.0 Ultimate" cmd /k "cd /d %~dp0 && python ultimate_v10_fixed.py"
timeout /t 2 /nobreak >nul

echo.
echo ? All services launched!
echo.
echo ?? Monitor with: python bin\monitor.py
echo.
echo ?? Quick Access:
echo    Analysis:  http://localhost:8007
echo    Visual:    http://localhost:8009
echo    Ultimate:  http://localhost:8013
echo.
pause
