
import os
import sys
import django

# Add project root to path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from problems.models import MathProblem
from problems.ai_solver import AISolver

def check_p30():
    try:
        p = MathProblem.objects.get(id=30)
        print(f"Problem 30 Extracted Text: '{p.extracted_text}'")
        
        solver = AISolver()
        
        # Test _solve_complex_arithmetic directly with this text
        res = solver._solve_complex_arithmetic(p.extracted_text)
        if res:
            print("\n_solve_complex_arithmetic SUCCEEDED!")
            print(f"Final Answer: {res['final_answer']}")
            for s in res['steps']:
                print(f"Step {s['step_number']}: {s['step_solution']}")
        else:
            print("\n_solve_complex_arithmetic FAILED (returned None)")
            
            # Debug why it failed
            import re
            clean_text = re.sub(r'^(calculate|solve|evaluate|find)\s+', '', p.extracted_text, flags=re.IGNORECASE).strip()
            print(f"Cleaned Text: '{clean_text}'")
            if not re.match(r'^[\d\+\-\*\/\(\)\.\=\s]+$', clean_text):
                print("REASON: Regex match failed")
                # Find the offending characters
                offenders = re.sub(r'[\d\+\-\*\/\(\)\.\=\s]', '', clean_text)
                print(f"Offending characters: '{offenders}' (hex: {[hex(ord(c)) for c in offenders]})")
            else:
                print("Regex match PASSED. Checking operators...")
                text_no_space = clean_text.replace(' ', '').replace('=', '')
                if not any(op in text_no_space for op in ['+', '-', '*', '/']):
                    print("REASON: No operators found in processing text")
                else:
                    print("Operators found. Tokenization might be the issue.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_p30()
