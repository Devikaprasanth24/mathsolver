import os
import django
import sys

# Setup django
sys.path.append('c:/Users/DEVIKA KP/OneDrive/math-solve')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from problems.solver import MathSolver
import json

problem = "2x + 4 = 10"
result = MathSolver.solve_problem(problem)
print(json.dumps(result, indent=2))
