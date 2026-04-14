"""
Quick script to generate .env file with proper SECRET_KEY
Run this: python setup_env.py
"""
import os
from django.core.management.utils import get_random_secret_key

env_content = f"""# Django Settings
SECRET_KEY={get_random_secret_key()}
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
# Use SQLite for quick development (no PostgreSQL setup needed)
USE_SQLITE=True

# PostgreSQL Settings (only needed if USE_SQLITE=False)
# DB_NAME=math_solve_db
# DB_USER=postgres
# DB_PASSWORD=your_postgres_password
# DB_HOST=localhost
# DB_PORT=5432

# AI API (optional - app will use mock solutions if not provided)
# OPENAI_API_KEY=your-openai-api-key-here
# ANTHROPIC_API_KEY=your-anthropic-api-key-here
# AI_PROVIDER=openai

# Static Files
STATIC_URL=/static/
MEDIA_URL=/media/
"""

if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ .env file created successfully!")
    print("📝 Using SQLite database (no PostgreSQL setup needed)")
    print("🔑 SECRET_KEY has been generated")
    print("\nYou can now run:")
    print("  python manage.py migrate")
    print("  python manage.py createsuperuser")
    print("  python manage.py runserver")
else:
    print("⚠️  .env file already exists. Delete it first if you want to regenerate.")
    response = input("Do you want to overwrite it? (yes/no): ")
    if response.lower() == 'yes':
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file updated successfully!")
    else:
        print("❌ Cancelled. Existing .env file preserved.")
