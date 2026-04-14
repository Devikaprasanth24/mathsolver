
import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from problems.ai_solver import AISolver
from problems.clue_generator import ClueGenerator
from problems.models import MathProblem, ProblemAttempt

def test_strict_output(problem_text):
    print(f"\n--- Testing: {problem_text} ---")
    solver = AISolver()
    solution = solver.solve_problem(problem_text)
    
    if not solution:
        print("FAILED: No solution generated")
        return

    print("Final Answer:", solution.get('final_answer'))
    print("Steps:")
    for step in solution.get('steps', []):
        print(f"  Step {step['step_number']} [{step['hint']}]: {step['step_solution']}")
        if step.get('explanation'):
            print(f"    WARNING: Explanation found: {step['explanation']}")

    # Test ClueGenerator
    problem, _ = MathProblem.objects.get_or_create(
        extracted_text=problem_text,
        defaults={'problem_type': 'arithmetic', 'difficulty': 'easy'}
    )
    problem.solution_steps = solution['steps']
    problem.final_answer = solution['final_answer']
    problem.save()
    
    from accounts.models import User
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com', 'is_student': True})
    attempt, _ = ProblemAttempt.objects.get_or_create(user=user, problem=problem)
    attempt.clues.all().delete()
    
    generator = ClueGenerator()
    generator.generate_clues_for_attempt(attempt)
    
    print("\nGenerated Clues:")
    for i, clue in enumerate(attempt.clues.all()):
        print(f"  Clue {i+1}: {clue.clue_text}")
        if "Formula" in clue.clue_text or "Identify" in clue.clue_text:
             if i == 0:
                 print("    ERROR: Formula/Intro step found in first clue!")

if __name__ == "__main__":
    test_strict_output("25% of 200")
    test_strict_output("1+2-3+5-2=")
    test_strict_output("Solve: 2x = 10")
