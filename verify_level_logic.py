import os
import django
import sys

# Setup django
sys.path.append('c:/Users/DEVIKA KP/OneDrive/math-solve')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from accounts.models import User
from problems.models import MathProblem, ProblemAttempt
from django.utils import timezone

# Get or create a test user
user, _ = User.objects.get_or_create(username='test_progress_user')
user.points = 0
user.level = 1
user.problem_attempts.all().delete()
user.save()

print(f"Initial: Level {user.level}, Solved {user.get_total_solved()}")

# Create a problem
problem = MathProblem.objects.create(
    extracted_text="1+1",
    final_answer="2",
    problem_type='arithmetic'
)

# Simulate solve
attempt = ProblemAttempt.objects.create(user=user, problem=problem)
attempt.mark_solved()

# Reload user
user.refresh_from_db()
print(f"After 1 solve: Level {user.level}, Solved {user.get_total_solved()}, Points {user.points}")
print(f"Average Hints: {user.get_average_hints()}")

if user.level == 2:
    print("SUCCESS: Level incremented to 2 after first solve.")
else:
    print(f"FAILURE: Level is {user.level}, expected 2.")
