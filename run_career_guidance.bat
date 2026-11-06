@echo off
title AI-Powered Career Guidance System - Hackathon Edition
echo ============================================================
echo   AI-POWERED CAREER GUIDANCE SYSTEM
echo   Launching Streamlit Web Application...
echo ============================================================
echo.
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    echo [INFO] Starting Streamlit server via virtual environment...
    ".venv\Scripts\python.exe" -m streamlit run app.py
) else (
    echo [INFO] Starting Streamlit server via system Python...
    python -m streamlit run app.py
)

pause
