@echo off
echo Killing any existing Python processes (py.exe)...
taskkill /F /IM py.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo Previous server instance killed.
) else (
    echo No previous server instance found.
)

echo Starting Loveca Simulator Server...
py server.py
