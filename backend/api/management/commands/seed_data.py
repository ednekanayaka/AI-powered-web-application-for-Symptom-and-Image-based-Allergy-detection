from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import ExercisePlan, MealPlan, UserProfile


class Command(BaseCommand):
    help = "Seeds admin user and initial meal/exercise plan data"

    def handle(self, *args, **kwargs):
        self._seed_admin()
        self._seed_meals()
        self._seed_exercises()

    def _seed_admin(self):
        email = "admin@gmail.com"
        password = "admin@123"

        user, created = User.objects.get_or_create(
            username=email,
            defaults={"email": email, "is_staff": True, "is_superuser": True}
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS("Admin user created"))
        else:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.WARNING("Admin user already exists; flags updated"))

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={"full_name": "System Admin", "is_admin": True}
        )

        if not profile.is_admin:
            profile.is_admin = True
            profile.full_name = profile.full_name or "System Admin"
            profile.save()
            self.stdout.write(self.style.SUCCESS("Admin profile updated"))
        else:
            self.stdout.write(self.style.SUCCESS("Admin profile ready"))

    def _seed_meals(self):
        if MealPlan.objects.exists():
            self.stdout.write(self.style.WARNING("MealPlan data already exists; skipped"))
            return

        meals = []

        general = [
            ("general", "Breakfast", 1, "Oatmeal with Banana", 350, "12g"),
            ("general", "Lunch", 1, "Grilled Chicken Salad", 450, "35g"),
            ("general", "Dinner", 1, "Vegetable Stir-fry with Rice", 400, "15g"),
            ("general", "Breakfast", 2, "Greek Yogurt with Berries", 300, "18g"),
            ("general", "Lunch", 2, "Turkey Sandwich on Whole Wheat", 420, "30g"),
            ("general", "Dinner", 2, "Baked Salmon with Vegetables", 480, "38g"),
            ("general", "Breakfast", 3, "Scrambled Eggs with Toast", 380, "22g"),
            ("general", "Lunch", 3, "Lentil Soup with Bread", 390, "20g"),
            ("general", "Dinner", 3, "Pasta with Tomato Sauce", 430, "16g"),
            ("general", "Breakfast", 4, "Smoothie Bowl", 320, "14g"),
            ("general", "Lunch", 4, "Quinoa Salad with Chickpeas", 410, "18g"),
            ("general", "Dinner", 4, "Grilled Fish Tacos", 460, "32g"),
            ("general", "Breakfast", 5, "Whole Wheat Pancakes", 340, "12g"),
            ("general", "Lunch", 5, "Caesar Salad with Shrimp", 380, "28g"),
            ("general", "Dinner", 5, "Beef Stew with Potatoes", 500, "35g"),
            ("general", "Breakfast", 6, "Avocado Toast with Eggs", 400, "20g"),
            ("general", "Lunch", 6, "Vegetable Wrap", 360, "14g"),
            ("general", "Dinner", 6, "Chicken Curry with Rice", 520, "40g"),
            ("general", "Breakfast", 7, "Fruit Salad with Nuts", 280, "8g"),
            ("general", "Lunch", 7, "Minestrone Soup", 350, "16g"),
            ("general", "Dinner", 7, "Grilled Vegetable Pizza", 440, "18g"),
        ]

        muscle = [
            ("muscle", "Breakfast", 1, "Protein Shake with Oats", 550, "45g"),
            ("muscle", "Lunch", 1, "Chicken Breast with Sweet Potato", 650, "55g"),
            ("muscle", "Dinner", 1, "Beef Steak with Broccoli", 700, "60g"),
            ("muscle", "Breakfast", 2, "Eggs and Whole Grain Toast", 500, "38g"),
            ("muscle", "Lunch", 2, "Tuna Pasta Salad", 600, "48g"),
            ("muscle", "Dinner", 2, "Salmon with Quinoa", 680, "52g"),
            ("muscle", "Breakfast", 3, "Cottage Cheese Pancakes", 480, "35g"),
            ("muscle", "Lunch", 3, "Turkey Meatballs with Pasta", 620, "50g"),
            ("muscle", "Dinner", 3, "Grilled Chicken with Brown Rice", 660, "58g"),
            ("muscle", "Breakfast", 4, "High Protein Smoothie", 520, "42g"),
            ("muscle", "Lunch", 4, "Beef Burrito Bowl", 680, "55g"),
            ("muscle", "Dinner", 4, "Pork Tenderloin with Vegetables", 640, "50g"),
            ("muscle", "Breakfast", 5, "Greek Yogurt Parfait", 450, "32g"),
            ("muscle", "Lunch", 5, "Shrimp Stir-fry with Rice", 580, "45g"),
            ("muscle", "Dinner", 5, "Chicken Thighs with Roasted Potatoes", 700, "56g"),
            ("muscle", "Breakfast", 6, "Protein Waffles", 500, "40g"),
            ("muscle", "Lunch", 6, "Lamb Chops with Couscous", 720, "58g"),
            ("muscle", "Dinner", 6, "Beef and Vegetable Stew", 660, "52g"),
            ("muscle", "Breakfast", 7, "Egg White Omelette", 380, "35g"),
            ("muscle", "Lunch", 7, "Chicken Caesar Wrap", 540, "45g"),
            ("muscle", "Dinner", 7, "Baked Cod with Asparagus", 580, "50g"),
        ]

        lose = [
            ("lose", "Breakfast", 1, "Green Smoothie", 220, "10g"),
            ("lose", "Lunch", 1, "Large Garden Salad with Tuna", 280, "25g"),
            ("lose", "Dinner", 1, "Grilled Chicken with Steamed Vegetables", 320, "35g"),
            ("lose", "Breakfast", 2, "Boiled Eggs with Fruit", 240, "18g"),
            ("lose", "Lunch", 2, "Vegetable Soup with Crackers", 260, "12g"),
            ("lose", "Dinner", 2, "Baked Tilapia with Salad", 300, "32g"),
            ("lose", "Breakfast", 3, "Low-fat Yogurt with Berries", 200, "14g"),
            ("lose", "Lunch", 3, "Turkey Lettuce Wraps", 270, "22g"),
            ("lose", "Dinner", 3, "Zucchini Noodles with Marinara", 280, "16g"),
            ("lose", "Breakfast", 4, "Chia Seed Pudding", 210, "8g"),
            ("lose", "Lunch", 4, "Grilled Shrimp Salad", 290, "28g"),
            ("lose", "Dinner", 4, "Stuffed Bell Peppers", 310, "20g"),
            ("lose", "Breakfast", 5, "Overnight Oats (Low Sugar)", 230, "11g"),
            ("lose", "Lunch", 5, "Cucumber and Avocado Salad", 250, "6g"),
            ("lose", "Dinner", 5, "Lemon Herb Chicken Breast", 330, "38g"),
            ("lose", "Breakfast", 6, "Egg White Scramble with Spinach", 220, "20g"),
            ("lose", "Lunch", 6, "Cauliflower Rice Bowl", 240, "14g"),
            ("lose", "Dinner", 6, "Baked Salmon with Cucumber Salad", 340, "36g"),
            ("lose", "Breakfast", 7, "Apple with Almond Butter", 210, "6g"),
            ("lose", "Lunch", 7, "Minestrone Soup (Low Sodium)", 230, "12g"),
            ("lose", "Dinner", 7, "Grilled White Fish with Asparagus", 290, "30g"),
        ]

        for goal_type, meal_type, day, name, calories, protein in general + muscle + lose:
            meals.append(
                MealPlan(
                    goal_type=goal_type,
                    meal_type=meal_type,
                    day=day,
                    name=name,
                    calories=calories,
                    protein=protein,
                )
            )

        MealPlan.objects.bulk_create(meals)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(meals)} MealPlan records"))

    def _seed_exercises(self):
        if ExercisePlan.objects.exists():
            self.stdout.write(self.style.WARNING("ExercisePlan data already exists; skipped"))
            return

        exercises = [
            ("general", "30-Min Brisk Walk", "1 session / 30 mins"),
            ("general", "Bodyweight Squats", "3 sets of 15 reps"),
            ("general", "Push-Ups", "3 sets of 12 reps"),
            ("general", "Plank Hold", "3 sets of 30 secs"),
            ("general", "Yoga Stretching", "20 mins"),
            ("muscle", "Barbell Bench Press", "4 sets of 8-10 reps"),
            ("muscle", "Deadlift", "4 sets of 6-8 reps"),
            ("muscle", "Pull-Ups", "4 sets of 8 reps"),
            ("muscle", "Overhead Press", "3 sets of 10 reps"),
            ("muscle", "Barbell Rows", "4 sets of 8 reps"),
            ("muscle", "Leg Press", "4 sets of 12 reps"),
            ("lose", "30-Min Jogging", "1 session / 30 mins"),
            ("lose", "Cycling", "45 mins"),
            ("lose", "Jump Rope", "3 rounds of 5 mins"),
            ("lose", "HIIT Circuit", "20 mins"),
            ("lose", "Swimming", "30 mins"),
            ("lose", "Burpees", "4 sets of 15 reps"),
        ]

        records = [
            ExercisePlan(goal_type=goal_type, name=name, sets=sets)
            for goal_type, name, sets in exercises
        ]
        ExercisePlan.objects.bulk_create(records)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(records)} ExercisePlan records"))
