
import os
import sys
import django

# Add project root to path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from problems.models import MathProblem, ProblemAttempt

def reset_all_for_exact_solutions():
    try:
        # Reset all arithmetic problems to ensure they use the new detailed solvers (arithmetic + percentage)
        problems = MathProblem.objects.filter(problem_type='arithmetic')
            
        print(f"Resetting {problems.count()} problems for exact solutions...")
        
        for p in problems:
            # Clear solution steps so it re-solves next time
            p.solution_steps = []
            p.final_answer = ""
            p.save()
            
            # Delete attempts so clues are re-generated
            ProblemAttempt.objects.filter(problem=p).delete()
            print(f"  Reset problem {p.id}: {p.extracted_text}")
            
        print("Done.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_all_for_exact_solutions()
