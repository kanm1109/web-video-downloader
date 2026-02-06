@echo off
echo ========================================
echo Starting Frontend Server...
echo ========================================
cd /d "%~dp0"
start http://localhost:3000
python -m http.server 3000
pause
