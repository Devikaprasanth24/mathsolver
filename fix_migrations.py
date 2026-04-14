"""
Fix migration history issue
Run this script to reset and fix migrations
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

print("Fixing migration history...")

# Delete migration history from django_migrations table
try:
    with connection.cursor() as cursor:
        # Delete all migration records
        cursor.execute("DELETE FROM django_migrations")
        print("Cleared migration history")
except Exception as e:
    print(f"Error: {e}")
    print("Trying to delete database file instead...")
    import os
    db_file = os.path.join(os.getcwd(), 'db.sqlite3')
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print("Database file deleted. Please run: python manage.py migrate")
        except Exception as e2:
            print(f"Cannot delete database: {e2}")
            print("Please close any programs using the database and delete db.sqlite3 manually")
    sys.exit(1)

print("\nRunning migrations...")
# Now run migrations fresh
call_command('migrate', verbosity=2)

print("\nMigrations completed successfully!")
print("\nYou can now run:")
print("  python manage.py createsuperuser")
print("  python manage.py runserver")
