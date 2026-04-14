# Math Solve - Learn to Think and Solve

A Django web application that helps students learn mathematics through a step-by-step clue system instead of providing direct answers. This platform encourages logical thinking and problem-solving skills.

## Features

### User Features
- **Math Scanner**: Upload images of math problems (handwritten or printed)
- **Step-by-Step Clues**: Receive progressive hints that guide thinking
- **Attempt Tracking**: Monitor your progress and attempts
- **Practice Mode**: Access curated practice problems
- **Rewards System**: Earn points, badges, and level up
- **Leaderboard**: Compete with other students

### Admin Features
- **User Management**: View and manage user accounts
- **Content Management**: Manage math problems and solutions
- **Progress Monitoring**: Track student progress and analytics
- **QR Code Generator**: Generate QR codes for math problems
- **Feedback & Support**: Manage user feedback and support requests

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL
- **Frontend**: Django Templates + HTMX + Alpine.js + Tailwind CSS
- **OCR**: pytesseract (Tesseract OCR)
- **AI**: OpenAI/Claude API for math problem solving
- **Image Processing**: Pillow (PIL)

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Tesseract OCR (for image text extraction)

### Setup Steps

1. **Clone the repository**
   ```bash
   cd math-solve
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR**
   - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `SECRET_KEY`: Django secret key
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`: PostgreSQL credentials
   - `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: AI API key
   - `AI_PROVIDER`: 'openai' or 'anthropic'

6. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE math_solve_db;
   ```

7. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - Frontend: http://127.0.0.1:8000/
    - Admin Panel: http://127.0.0.1:8000/admin/

## Project Structure

```
math-solve/
├── accounts/          # User authentication and profiles
├── scanner/           # Image upload and OCR processing
├── problems/          # Problem solving and clue system
├── admin_panel/       # Admin dashboard and management
├── math_solve/        # Main Django project settings
├── templates/         # HTML templates
├── static/            # Static files (CSS, JS)
├── media/             # Uploaded images
└── requirements.txt   # Python dependencies
```

## Usage

### For Students

1. **Sign Up**: Create an account
2. **Scan Problem**: Upload an image of a math problem
3. **Get Clues**: Receive step-by-step hints progressively
4. **Solve**: Work through the problem with guidance
5. **Earn Points**: Get rewarded for solving with fewer hints

### For Admins

1. **Access Admin Panel**: Login as staff user
2. **Manage Users**: View user statistics and progress
3. **Manage Content**: Add/edit math problems
4. **Generate QR Codes**: Create QR codes for problems
5. **Monitor Progress**: Track student performance

## Security Features

- CSRF protection enabled
- File upload validation (type and size limits)
- SQL injection prevention (Django ORM)
- XSS protection in templates
- Authentication required for all problem-solving features
- Admin-only access for admin panel

## Math Problem Validation

The system validates uploaded images to ensure they contain math problems:
- Rejects physics, chemistry, and text-based questions
- Validates math keywords and symbols
- Checks for mathematical expressions

## AI Integration

The platform uses AI (OpenAI or Claude) to:
- Solve math problems step-by-step
- Generate progressive hints/clues
- Extract formulas and solution steps
- Provide educational explanations

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## Environment Variables

See `.env.example` for all required environment variables.

## License

This project is for educational purposes.

## Support

For issues or feedback, use the feedback form in the application or contact the admin.
