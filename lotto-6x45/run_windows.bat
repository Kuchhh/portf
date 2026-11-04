@echo off
chcp 65001 >nul
cd /d "%~dp0"
python gosloto645.py %*
if errorlevel 9009 py gosloto645.py %*
pause
