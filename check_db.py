import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from accounts.models import User
from problems.models import ProblemAttempt

def check_users():
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    for user in users:
        print(f"User: {user.username}, Points: {user.points}, Level: {user.level}, Is Student: {user.is_student}")
        attempts = ProblemAttempt.objects.filter(user=user)
        print(f"  Attempts: {attempts.count()}, Solved: {attempts.filter(solved=True).count()}")

if __name__ == "__main__":
    check_users()
