import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import ExercisePlan

def seed_exercises():
    goals = ["general", "lose", "gain", "muscle"]
    exercises = [
        ("Morning Walk", "30 mins"),
        ("Yoga & Stretching", "45 mins"),
        ("Full Body Workout", "4 sets x 12 reps"),
        ("Cardio / Running", "20 mins"),
        ("Leg Day", "4 sets x 10 reps"),
        ("Core & Abs", "3 sets x 15 reps"),
        ("Rest & Recovery", "Light Stretching")
    ]

    created = 0
    updated = 0

    for goal in goals:
        for i, (name, sets) in enumerate(exercises):
            plan_name = f"Day {i+1}: {name}"
            _, was_created = ExercisePlan.objects.update_or_create(
                goal_type=goal,
                name=plan_name,
                defaults={
                    "sets": sets,
                    "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=600&q=80",
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

    print(f"Seeded exercises. created={created}, updated={updated}")

if __name__ == "__main__":
    seed_exercises()
