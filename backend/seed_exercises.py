import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import ExercisePlan

def seed_exercises():
    # Clear existing
    ExercisePlan.objects.all().delete()
    print("Cleared existing exercises.")

    plans = []
    goals = ["lose", "gain", "muscle"]
    exercises = [
        ("Morning Walk", "30 mins"),
        ("Yoga & Stretching", "45 mins"),
        ("Full Body Workout", "4 sets x 12 reps"),
        ("Cardio / Running", "20 mins"),
        ("Leg Day", "4 sets x 10 reps"),
        ("Core & Abs", "3 sets x 15 reps"),
        ("Rest & Recovery", "Light Stretching")
    ]

    for goal in goals:
        for i, (name, sets) in enumerate(exercises):
            plans.append(ExercisePlan(
                goal_type=goal,
                name=f"Day {i+1}: {name}",
                sets=sets,
                image_url=f"https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=600&q=80"
            ))

    ExercisePlan.objects.bulk_create(plans)
    print(f"Seeded {len(plans)} exercises.")

if __name__ == "__main__":
    seed_exercises()
