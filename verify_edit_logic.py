import os
import django
import sys

# Setup django
sys.path.append('c:/Users/DEVIKA KP/OneDrive/math-solve')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from problems.models import MathProblem

# Get a problem
problem = MathProblem.objects.first()
if not problem:
    print("No problems found to test.")
    sys.exit(0)

original_diff = problem.difficulty
new_diff = 'hard' if original_diff != 'hard' else 'easy'

print(f"Original Difficulty: {original_diff}")
print(f"Updating to: {new_diff}")

problem.difficulty = new_diff
problem.save()

problem.refresh_from_db()
print(f"Updated Difficulty: {problem.difficulty}")

if problem.difficulty == new_diff:
    print("SUCCESS: Difficulty updated successfully in database.")
    # Revert to original for cleanliness
    problem.difficulty = original_diff
    problem.save()
else:
    print("FAILURE: Difficulty did not update.")
