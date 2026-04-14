# Setup Guide for Math Solve

## Quick Start

### 1. Install System Dependencies

**Tesseract OCR** (Required for image text extraction):

- **Windows**: Download installer from https://github.com/UB-Mannheim/tesseract/wiki
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

**PostgreSQL** (Database):

- Download and install from https://www.postgresql.org/download/

### 2. Python Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### 3. Database Setup

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE math_solve_db;

-- Create user (optional)
CREATE USER math_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE math_solve_db TO math_user;
```

### 4. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings:
# - SECRET_KEY (generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
# - Database credentials
# - OpenAI or Anthropic API key
```

### 5. Django Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Access the application at http://127.0.0.1:8000/

## First Steps After Setup

1. **Login as Admin**: Use the superuser account you created
2. **Create Test Problems**: Go to Admin Panel → Content Management
3. **Test Scanner**: Upload a math problem image
4. **Test Solving**: Try solving a problem and revealing clues

## Troubleshooting

### Tesseract Not Found
- Make sure Tesseract is installed and in your PATH
- On Windows, you may need to set the path in settings:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### Database Connection Error
- Verify PostgreSQL is running
- Check database credentials in .env file
- Ensure database exists

### AI API Errors
- Verify API key is set correctly in .env
- Check API provider (openai or anthropic)
- Ensure you have API credits/quota

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check STATIC_URL and STATIC_ROOT in settings.py
- Ensure DEBUG=True for development

## Production Deployment

1. Set `DEBUG=False` in .env
2. Set proper `ALLOWED_HOSTS`
3. Use a production WSGI server (gunicorn, uwsgi)
4. Set up a reverse proxy (nginx, Apache)
5. Configure static file serving
6. Use environment variables for secrets
7. Set up SSL/HTTPS

## Notes

- The application requires an AI API key (OpenAI or Anthropic) for problem solving
- Tesseract OCR is required for image text extraction
- PostgreSQL is required (SQLite can be used for development but not recommended)
- Media files are stored in the `media/` directory
