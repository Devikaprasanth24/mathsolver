@echo off
REM Quick run script for Windows
echo Starting Math Solve Development Server...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.
echo Running migrations...
python manage.py migrate

echo.
echo Starting development server...
echo Server will be available at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver

pause
