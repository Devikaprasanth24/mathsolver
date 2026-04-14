#!/bin/bash
# Quick run script for macOS/Linux

echo "Starting Math Solve Development Server..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "Running migrations..."
python manage.py migrate

echo ""
echo "Starting development server..."
echo "Server will be available at http://127.0.0.1:8000/"
echo "Press Ctrl+C to stop the server"
echo ""
python manage.py runserver
