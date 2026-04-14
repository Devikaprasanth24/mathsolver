
import os
import sys
import django

# Add project root to path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from problems.models import MathProblem

def dump_problem(problem_id):
    try:
        problem = MathProblem.objects.get(id=problem_id)
        print(f"Problem ID: {problem.id}")
        print(f"Extracted Text: '{problem.extracted_text}'")
        print(f"Problem Type: {problem.problem_type}")
        print(f"Difficulty: {problem.difficulty}")
        print(f"Final Answer: '{problem.final_answer}'")
        print(f"Solution Steps: {problem.solution_steps}")
        print(f"Understanding: {problem.problem_understanding}")
    except MathProblem.DoesNotExist:
        print(f"Problem {problem_id} not found.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dump_problem(sys.argv[1])
    else:
        # Check some recent problems
        for p in MathProblem.objects.all()[:5]:
            dump_problem(p.id)
            print("-" * 20)
