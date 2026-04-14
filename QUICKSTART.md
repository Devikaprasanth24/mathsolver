# Quick Start Guide - Math Solve

## Prerequisites

Before running the application, make sure you have:

1. **Python 3.8+** installed
2. **PostgreSQL** installed and running
3. **Tesseract OCR** installed (for image text extraction)

## Step-by-Step Setup

### 1. Install System Dependencies

#### Install Tesseract OCR

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Install and note the installation path (usually `C:\Program Files\Tesseract-OCR`)

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### Install PostgreSQL

- Download from: https://www.postgresql.org/download/
- Or use package manager:
  - **macOS**: `brew install postgresql`
  - **Linux**: `sudo apt-get install postgresql postgresql-contrib`

### 2. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE math_solve_db;

# Create user (optional, or use default postgres user)
CREATE USER math_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE math_solve_db TO math_user;
\q
```

### 3. Set Up Python Environment

```bash
# Navigate to project directory
cd "c:\Users\DEVIKA KP\OneDrive\math-solve"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example environment file
copy .env.example .env
# On macOS/Linux: cp .env.example .env

# Edit .env file with your settings
```

Edit the `.env` file with these values:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (use your PostgreSQL credentials)
DB_NAME=math_solve_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

# AI API (choose one)
OPENAI_API_KEY=your-openai-api-key-here
# OR
ANTHROPIC_API_KEY=your-anthropic-api-key-here
AI_PROVIDER=openai  # or 'anthropic'

# Static Files
STATIC_URL=/static/
MEDIA_URL=/media/
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Configure Tesseract Path (Windows only)

If Tesseract is not in your PATH, edit `scanner/utils.py` and add at the top:

```python
import pytesseract

# Windows - Update this path to your Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 6. Run Database Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

### 7. Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 8. Collect Static Files (Optional for development)

```bash
python manage.py collectstatic
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

## Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **User Dashboard**: http://127.0.0.1:8000/problems/ (after login)

## First Steps

1. **Login as Admin**: Use the superuser account you created
2. **Create Test User**: Sign up at http://127.0.0.1:8000/signup/
3. **Test Scanner**: 
   - Login as user
   - Go to Scanner page
   - Upload a math problem image
4. **Test Problem Solving**:
   - After scanning, you'll be redirected to solve the problem
   - Click "Reveal Next Clue" to see progressive hints

## Troubleshooting

### "Tesseract not found" error
- Make sure Tesseract is installed
- On Windows, set the path in `scanner/utils.py` (see step 5)
- Verify installation: `tesseract --version`

### Database connection error
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists: `psql -U postgres -l` (should list `math_solve_db`)

### "No module named 'django'" error
- Make sure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`

### AI API errors
- Verify API key is correct in `.env`
- Check you have API credits/quota
- For development, the app will use mock solutions if API fails

### Static files not loading
- Run: `python manage.py collectstatic`
- Check `DEBUG=True` in `.env` for development

### Port already in use
- Use a different port: `python manage.py runserver 8001`

## Development Notes

- **Debug Mode**: Set `DEBUG=True` in `.env` for development
- **Media Files**: Uploaded images are stored in `media/` directory
- **Database**: Uses PostgreSQL (can use SQLite for testing by changing settings.py)
- **AI Provider**: Switch between OpenAI and Anthropic in `.env`

## Production Deployment

For production:
1. Set `DEBUG=False` in `.env`
2. Set proper `ALLOWED_HOSTS`
3. Use a production WSGI server (gunicorn, uwsgi)
4. Set up reverse proxy (nginx, Apache)
5. Configure static file serving
6. Use environment variables for all secrets
7. Set up SSL/HTTPS

## Need Help?

- Check `README.md` for detailed documentation
- Check `SETUP.md` for more setup details
- Review error messages in terminal/console
