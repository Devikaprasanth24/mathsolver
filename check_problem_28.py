
import os
import sys
import django

# Add project root to path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from problems.models import MathProblem
from problems.ai_solver import AISolver

def check_p28():
    try:
        # Check if 25% of 200 or 29% of 200
        # The user seems to have problems with both
        test_cases = ["25% of 200 = ?", "29% of 200 = ", "25% of 200", "29% of 200"]
        
        solver = AISolver()
        
        for case in test_cases:
            print(f"\n--- Testing Case: '{case}' ---")
            res = solver._mock_solution(case) # This calls _solve_percentage_specific
            if res and 'steps' in res and len(res['steps']) > 0 and 'hint' in res['steps'][0] and "Convert the percentage" in res['steps'][0]['hint']:
                print("SUCCESS: Exact solution generated!")
                print(f"Final Answer: {res['final_answer']}")
                for s in res['steps']:
                    print(f"Step {s['step_number']}: {s['step_solution']}")
            else:
                print("FAILED: Generic hints or no solution returned")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_p28()
