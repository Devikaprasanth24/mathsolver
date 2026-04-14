import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=['problems'],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}},
    )
    django.setup()

from problems.models import MathProblem

# Find the problem
# We search for problems containing "2+35" to be sure
problems = MathProblem.objects.filter(extracted_text__contains="2")
count = 0

print("Searching for problems...")
for p in problems:
    # Check relatively broad match
    if "35" in p.extracted_text and "45" in p.extracted_text:
        print(f"Found problem ID {p.id}: {p.extracted_text}")
        print("Clearing solution steps...")
        p.solution_steps = [] # Clear the steps
        p.final_answer = ""
        p.save()
        count += 1

if count > 0:
    print(f"Successfully cleared cache for {count} problem(s).")
else:
    print("No matching problems found to clear.")
