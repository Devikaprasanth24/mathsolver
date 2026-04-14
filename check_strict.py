
import os
import sys
import django

# Add project root to path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from problems.models import MathProblem
from problems.ai_solver import AISolver

def check_p28_strict():
    try:
        test_cases = ["25% of 200 = ?", "29% of 200", "1+2-3+5-2="]
        
        solver = AISolver()
        
        for case in test_cases:
            print(f"\n--- Testing Case: '{case}' ---")
            res = solver._mock_solution(case) 
            if res and 'steps' in res and len(res['steps']) > 0:
                print("SUCCESS: Steps generated!")
                print(f"Final Answer: {res['final_answer']}")
                
                # Verify NO generic rules text
                generic_rules = ["PEMDAS", "BODMAS", "According to", "Order of Operations", "Next, perform"]
                found_generic = False
                for s in res['steps']:
                    print(f"  Step {s['step_number']} [{s['hint']}]: {s['step_solution']}")
                    for rule in generic_rules:
                        if rule.lower() in s['hint'].lower() or rule.lower() in s.get('explanation', '').lower():
                            print(f"  !!! WARNING: Found theory text: '{rule}'")
                            found_generic = True
                
                if not found_generic:
                    print("  STRICT STYLE VERIFIED: No theory text found.")
            else:
                print("FAILED: No steps returned")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_p28_strict()
