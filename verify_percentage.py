
import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from problems.ai_solver import AISolver

def test_percentage():
    solver = AISolver()
    res = solver._solve_percentage_specific("25% of 200")
    if res:
        print("\n--- 25% of 200 ---")
        for step in res['steps']:
            print(f"Step {step['step_number']}: {step['hint']} {step['step_solution']}")
        print("Final Answer:", res['final_answer'])

if __name__ == "__main__":
    test_percentage()
