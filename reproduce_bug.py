
import os
import sys

# Mock settings for AISolver
os.environ['AI_PROVIDER'] = 'openai'
os.environ['OPENAI_API_KEY'] = 'mock'

from problems.ai_solver import AISolver

def test_repro():
    solver = AISolver()
    problem_text = "1+2-3+5-2="
    
    print(f"Testing problem: {problem_text}")
    
    # Test _solve_complex_arithmetic directly
    print("\n--- Testing _solve_complex_arithmetic ---")
    try:
        res = solver._solve_complex_arithmetic(problem_text)
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")

    # Test _generate_final_answer directly
    print("\n--- Testing _generate_final_answer ---")
    import re
    numbers = re.findall(r'[-+]?[\d]*\.?[\d]+', problem_text)
    print(f"Numbers extracted: {numbers}")
    res = solver._generate_final_answer(problem_text, 'arithmetic', numbers)
    print(f"Final Answer returned: {res}")

    # Test _mock_solution
    print("\n--- Testing _mock_solution ---")
    res = solver._mock_solution(problem_text)
    print(f"Mock Final Answer: {res.get('final_answer')}")

if __name__ == "__main__":
    # Add parent dir to path to import problems
    sys.path.append(os.getcwd())
    test_repro()
