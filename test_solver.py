import os
import django
from django.conf import settings

# Configure Django settings manually since we're running a standalone script
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=['problems'],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': 'db.sqlite3'}},
    )
    django.setup()

from problems.ai_solver import AISolver

solver = AISolver()
problem = "2+35-45+2=" # Added = to simulate user input failure case
print(f"Testing problem: {problem}")

# Test the complex arithmetic solver specifically
result = solver._solve_complex_arithmetic(problem)

if result:
    print("SUCCESS! Solution found:")
    import json
    print(json.dumps(result, indent=2))
else:
    print("FAILED. No solution returned.")
