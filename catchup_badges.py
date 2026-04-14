import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from accounts.models import User

def catch_up_badges():
    users = User.objects.all()
    print(f"Checking {users.count()} users for badges...")
    for user in users:
        user.check_and_award_badges()
        print(f"Processed {user.username}: Badges = {user.userbadge_set.count()}")

if __name__ == "__main__":
    catch_up_badges()
