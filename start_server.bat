@echo off
echo ========================================
echo MyTravel Backend Server Startup
echo ========================================
echo.

cd /d "%~dp0"

echo Checking virtual environment...
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo Starting Django Development Server
echo ========================================
echo.
echo Backend will be available at:
echo   - API: http://localhost:8000/api
echo   - Admin: http://localhost:8000/admin
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver

pause
