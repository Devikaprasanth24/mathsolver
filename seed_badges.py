import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'math_solve.settings')
django.setup()

from accounts.models import Badge

def seed_badges():
    badges = [
        {
            'badge_type': 'first_solve',
            'name': 'Pioneer',
            'description': 'Solved your first math problem!',
            'icon': '🚀'
        },
        {
            'badge_type': 'persistent',
            'name': 'Marathoner',
            'description': 'Solved 10 problems!',
            'icon': '🏃'
        },
        {
            'badge_type': 'expert',
            'name': 'Math Expert',
            'description': 'Reached Level 5!',
            'icon': '🧠'
        },
        {
            'badge_type': 'quick_solver',
            'name': 'Speedster',
            'description': 'Solved a problem in under 30 seconds!',
            'icon': '⚡'
        },
        {
            'badge_type': 'perfect',
            'name': 'Perfectionist',
            'description': 'Solved a problem without any hints!',
            'icon': '💎'
        },
    ]

    for b_data in badges:
        badge, created = Badge.objects.get_or_create(
            badge_type=b_data['badge_type'],
            defaults={
                'name': b_data['name'],
                'description': b_data['description'],
                'icon': b_data['icon']
            }
        )
        if created:
            print(f"Created badge: {badge.name}")
        else:
            print(f"Badge already exists: {badge.name}")

if __name__ == "__main__":
    seed_badges()
