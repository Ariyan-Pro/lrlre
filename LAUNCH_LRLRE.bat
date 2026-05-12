@echo off
cls
echo ======================================================
echo    ?? LRLRE ENTERPRISE GRID - ONE CLICK LAUNCHER
echo ======================================================
echo.
echo This will launch ALL THREE versions:
echo   ?? v7.0 Analysis Grid  (port 8007)
echo   ?? v8.2 Visual Grid    (port 8009)
echo   ?? v10.0 Ultimate Grid (port 8013)
echo.
echo ======================================================
echo.

cd /d "%~dp0"

echo ?? Checking for existing processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8007') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8009') do taskkill /F /PID %%a 2>nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8013') do taskkill /F /PID %%a 2>nul
timeout /t 2 /nobreak >nul

echo.
echo ?? Launching services...
echo.

start "LRLRE v7.0" cmd /k "cd /d %~dp0 && echo === v7.0 ANALYSIS GRID === && echo Port: 8007 && echo. && python start_analytics_v7.py"
timeout /t 2 /nobreak >nul

start "LRLRE v8.2" cmd /k "cd /d %~dp0 && echo === v8.2 VISUAL GRID === && echo Port: 8009 && echo. && python start_analytics_v8_bento_grid.py"
timeout /t 2 /nobreak >nul

start "LRLRE v10.0" cmd /k "cd /d %~dp0 && echo === v10.0 ULTIMATE GRID === && echo Port: 8013 && echo. && python ultimate_v10_fixed.py"

echo.
echo ======================================================
echo ? ALL SERVICES LAUNCHED SUCCESSFULLY!
echo ======================================================
echo.
echo ?? Monitor: python bin\monitor.py
echo.
echo ?? ACCESS AT:
echo    ?? Analysis:  http://localhost:8007
echo    ?? Visual:    http://localhost:8009
echo    ?? Ultimate:  http://localhost:8013
echo.
echo ======================================================
echo.
pause
