@echo off
title Graveyard Locator - Launcher
color 0A

echo.
echo  ============================================
echo   GRAVEYARD LOCATOR - STARTUP
echo  ============================================
echo.

:: ── Check Python ──────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found.
    echo  Please install Python 3.12 from https://python.org
    echo  Make sure to tick "Add Python to PATH" during install.
    pause
    exit /b 1
)

echo  [OK] Python found.

:: ── Go to script's own folder ─────────────────
cd /d "%~dp0"

:: ── Install dependencies ──────────────────────
echo.
echo  [INFO] Installing / checking requirements...
echo.
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo  [ERROR] Failed to install requirements.
    echo  Try running this file as Administrator.
    pause
    exit /b 1
)

echo.
echo  [OK] All packages ready.

:: ── Init database ─────────────────────────────
echo  [INFO] Initialising database...
python -c "from database.db_setup import initialize_database; initialize_database()"
if errorlevel 1 (
    echo  [WARN] Database init returned an error - continuing anyway.
)
echo  [OK] Database ready.

:: ── Launch app ────────────────────────────────
echo.
echo  ============================================
echo   Starting Streamlit app...
echo   Open your browser at: http://localhost:8501
echo   Press Ctrl+C in this window to stop.
echo  ============================================
echo.

python -m streamlit run app.py

pause
