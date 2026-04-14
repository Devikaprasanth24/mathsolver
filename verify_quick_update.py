import os
import django
import sys

# Setup django - MUST be before any django imports
sys.path.append('c:/Users/DEVIKA KP/OneDrive/math-solve')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from problems.models import MathProblem
from admin_panel.views import quick_update_difficulty
from accounts.models import User

# Mock request
factory = RequestFactory()
problem = MathProblem.objects.first()

if not problem:
    print("No problems found.")
    sys.exit(0)

# Create/Get a mock admin user
admin_user = User.objects.filter(is_staff=True).first()
if not admin_user:
    admin_user = User.objects.create_superuser('temp_admin_2', 'admin2@test.com', 'password123')
    created_admin = True
else:
    created_admin = False

print(f"Testing Quick Update for Problem {problem.id}")
print(f"Current Difficulty: {problem.difficulty}")

# Test updating to a different level
original_diff = problem.difficulty
new_diff = 'hard' if original_diff != 'hard' else 'easy'

request = factory.post(f'/admin-panel/problems/quick-difficulty/{problem.id}/', {'difficulty': new_diff})
request.user = admin_user

response = quick_update_difficulty(request, problem.id)

problem.refresh_from_db()

if response.status_code == 200 and problem.difficulty == new_diff:
    print(f"SUCCESS: Difficulty updated to {new_diff} and returned 200 OK.")
    # Revert
    problem.difficulty = original_diff
    problem.save()
else:
    print(f"FAILURE: Update failed. Code: {response.status_code}, DB Diff: {problem.difficulty}")

# Cleanup
if created_admin:
    admin_user.delete()
