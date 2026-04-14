
import os
import sys
import django

# Setup Django environment
sys.path.append('c:/Users/DEVIKA KP/OneDrive/math-solve')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from math_api.llm import solve_with_llm

def test_solver(problem):
    print(f"\nTesting problem: {problem}")
    result = solve_with_llm("Math Problem", "Medium", problem)
    print("AI Result:")
    print(f"Final Answer: {result.get('final_answer')}")
    print("Steps:")
    for step in result.get('steps', []):
        print(f" - {step}")
    
    # Check if steps look generalized or mathematical
    generalized_keywords = ["PEMDAS", "BODMAS", "Identify", "Substitute", "Simplify", "formula"]
    has_generalized = any(any(kw.lower() in step.lower() for kw in generalized_keywords) for step in result.get('steps', []))
    
    if has_generalized:
        print("\nWARNING: Steps still contain generalized text.")
    else:
        print("\nSUCCESS: Steps are direct calculations.")

if __name__ == "__main__":
    test_solver("2x + 5 = 15")
    test_solver("29% of 200")
