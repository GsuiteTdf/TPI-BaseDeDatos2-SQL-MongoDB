@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0backup_tpi.ps1"
if errorlevel 1 (
    echo.
    echo El resguardo fallo.
    pause
    exit /b 1
)
echo.
pause
