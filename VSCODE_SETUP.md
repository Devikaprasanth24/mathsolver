# Running Math Solve in VS Code

This guide will help you set up and run the Django application in Visual Studio Code.

## Prerequisites

1. **VS Code Extensions** - Install these extensions:
   - Python (by Microsoft)
   - Django (by Baptiste Darthenay) - Optional but helpful
   - Python Debugger (by Microsoft)

2. **Install Extensions:**
   - Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on Mac)
   - Search and install:
     - `Python`
     - `Django` (optional)

## Step-by-Step Setup

### 1. Open Project in VS Code

```bash
# Open VS Code in the project directory
code "c:\Users\DEVIKA KP\OneDrive\math-solve"
```

Or:
- Open VS Code
- File → Open Folder
- Select the `math-solve` folder

### 2. Select Python Interpreter

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: `Python: Select Interpreter`
3. Choose the interpreter from your virtual environment:
   - `.\venv\Scripts\python.exe` (Windows)
   - `./venv/bin/python` (Mac/Linux)

**If virtual environment doesn't exist yet:**
```bash
# In VS Code terminal (Ctrl+` to open)
python -m venv venv
```

### 3. Install Dependencies

Open the integrated terminal in VS Code (`Ctrl+` ` or View → Terminal`):

```bash
# Activate virtual environment (if not auto-activated)
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
venv\Scripts\activate.bat     # Windows CMD

# Install packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env` in the root directory
2. Edit `.env` with your settings (database, API keys, etc.)

### 5. Run Database Migrations

In the VS Code terminal:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (First Time Only)

```bash
python manage.py createsuperuser
```

## Running the Application

### Method 1: Using VS Code Terminal (Recommended)

1. Open terminal: `Ctrl+` ` (backtick) or View → Terminal
2. Activate virtual environment (if not auto-activated):
   ```bash
   .\venv\Scripts\Activate.ps1
   ```
3. Run server:
   ```bash
   python manage.py runserver
   ```
4. Access at: http://127.0.0.1:8000/

### Method 2: Using VS Code Debugger

1. Go to Run and Debug panel: `Ctrl+Shift+D`
2. Select "Python: Django" from dropdown
3. Click the green play button (or press `F5`)
4. Server will start automatically
5. Access at: http://127.0.0.1:8000/

### Method 3: Using Task Runner

1. Press `Ctrl+Shift+P`
2. Type: `Tasks: Run Task`
3. Select "Django: Run Server" (if configured)

## VS Code Terminal Commands

### Quick Commands Reference

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Run Django shell
python manage.py shell

# Run tests
python manage.py test
```

## Debugging in VS Code

### Setting Breakpoints

1. Click in the left margin next to line numbers to set breakpoints
2. Red dots will appear indicating breakpoints
3. Start debugging with `F5`
4. Execution will pause at breakpoints

### Debug Configuration

The `.vscode/launch.json` file is already configured. You can:
- Add more breakpoints
- Step through code (F10 - step over, F11 - step into)
- Inspect variables in the Debug panel

### Common Debug Scenarios

**Debug a specific view:**
1. Open the view file (e.g., `accounts/views.py`)
2. Set breakpoint in the function
3. Start debugger (`F5`)
4. Trigger the view in browser
5. VS Code will pause at the breakpoint

## VS Code Tips

### 1. Multiple Terminals

You can open multiple terminals:
- Click the `+` button in terminal panel
- Or: `Ctrl+Shift+` ` (backtick)

Useful for:
- One terminal for server
- Another for migrations/commands

### 2. Integrated Terminal Shortcuts

- `Ctrl+` ` - Toggle terminal
- `Ctrl+Shift+` ` - New terminal
- `Ctrl+Shift+C` - Copy in terminal
- `Ctrl+Shift+V` - Paste in terminal

### 3. Python Environment

VS Code should auto-detect your virtual environment. If not:
- Check bottom-right corner for Python version
- Click to change interpreter
- Select `.\venv\Scripts\python.exe`

### 4. Django Template Support

VS Code will provide syntax highlighting for Django templates. For better IntelliSense:
- Install "Django" extension
- Templates will have syntax highlighting

### 5. Git Integration

VS Code has built-in Git support:
- View changes in Source Control panel (`Ctrl+Shift+G`)
- Stage, commit, and push directly from VS Code

## Troubleshooting

### "Python not found" error

1. Install Python extension
2. Select correct interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose virtual environment Python

### Terminal not activating virtual environment

1. Check `.vscode/settings.json` has:
   ```json
   "python.terminal.activateEnvironment": true
   ```
2. Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"

### Import errors in VS Code

1. Make sure virtual environment is selected
2. Install packages: `pip install -r requirements.txt`
3. Reload VS Code window

### Debugger not working

1. Check `.vscode/launch.json` exists
2. Make sure Python extension is installed
3. Verify `django` is in `INSTALLED_APPS` in settings.py

### Port already in use

If port 8000 is busy:
```bash
python manage.py runserver 8001
```

Or change in `.vscode/launch.json`:
```json
"args": ["runserver", "127.0.0.1:8001"]
```

## Recommended VS Code Extensions

- **Python** - Core Python support
- **Django** - Django template support
- **Python Docstring Generator** - Auto-generate docstrings
- **Error Lens** - Show errors inline
- **GitLens** - Enhanced Git capabilities
- **Prettier** - Code formatter (optional)

## Quick Start Checklist

- [ ] Open project in VS Code
- [ ] Install Python extension
- [ ] Create/activate virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Configure `.env` file
- [ ] Run migrations (`python manage.py migrate`)
- [ ] Create superuser (`python manage.py createsuperuser`)
- [ ] Start server (`python manage.py runserver` or F5)
- [ ] Open http://127.0.0.1:8000/ in browser

## Next Steps

Once running:
1. Access admin panel: http://127.0.0.1:8000/admin/
2. Create test user: http://127.0.0.1:8000/signup/
3. Test scanner: http://127.0.0.1:8000/scanner/upload/

Happy coding! 🚀
