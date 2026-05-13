from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from collections import defaultdict

from api.image_catalog import get_image_url_for_title
from api.models import ExercisePlan, MealPlan, UserProfile


class Command(BaseCommand):
    help = "Seeds admin user and initial meal/exercise plan data"

    def handle(self, *args, **kwargs):
        self._seed_admin()
        self._dedupe_meals()
        self._dedupe_exercises()
        self._seed_meals()
        self._seed_exercises()
        self._repair_random_image_sources()

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

    def _default_image(self, name, kind="meal"):
        return get_image_url_for_title(name, kind=kind)

    def _seed_meals(self):
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

        created = 0
        updated = 0
        for goal_type, meal_type, day, name, calories, protein in general + muscle + lose:
            _, was_created = MealPlan.objects.update_or_create(
                goal_type=goal_type,
                meal_type=meal_type,
                day=day,
                defaults={
                    "name": name,
                    "calories": calories,
                    "protein": protein,
                    "image_url": self._default_image(name, "meal"),
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Meal plans seeded. created={created}, updated={updated}"))

    def _seed_exercises(self):
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

        created = 0
        updated = 0
        for goal_type, name, sets in exercises:
            _, was_created = ExercisePlan.objects.update_or_create(
                goal_type=goal_type,
                name=name,
                defaults={
                    "sets": sets,
                    "image_url": self._default_image(name, "exercise"),
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Exercise plans seeded. created={created}, updated={updated}"))

    def _dedupe_meals(self):
        grouped = defaultdict(list)
        for meal in MealPlan.objects.all().order_by("id"):
            key = (meal.goal_type, meal.day, (meal.meal_type or "").strip().lower())
            grouped[key].append(meal)

        deleted = 0
        for rows in grouped.values():
            if len(rows) <= 1:
                continue

            ranked = sorted(
                rows,
                key=lambda row: (0 if (row.image_url and str(row.image_url).strip()) else 1, row.id),
            )

            for duplicate in ranked[1:]:
                duplicate.delete()
                deleted += 1

        if deleted:
            self.stdout.write(self.style.WARNING(f"Deduplicated meal rows: removed={deleted}"))
        else:
            self.stdout.write(self.style.SUCCESS("No duplicate meal rows found"))

    def _dedupe_exercises(self):
        grouped = defaultdict(list)
        for exercise in ExercisePlan.objects.all().order_by("id"):
            key = (exercise.goal_type, (exercise.name or "").strip().lower())
            grouped[key].append(exercise)

        deleted = 0
        for rows in grouped.values():
            if len(rows) <= 1:
                continue

            ranked = sorted(
                rows,
                key=lambda row: (0 if (row.image_url and str(row.image_url).strip()) else 1, row.id),
            )

            for duplicate in ranked[1:]:
                duplicate.delete()
                deleted += 1

        if deleted:
            self.stdout.write(self.style.WARNING(f"Deduplicated exercise rows: removed={deleted}"))
        else:
            self.stdout.write(self.style.SUCCESS("No duplicate exercise rows found"))

    def _repair_random_image_sources(self):
        random_hosts = ("loremflickr.com", "source.unsplash.com", "picsum.photos")

        meal_fixed = 0
        for meal in MealPlan.objects.all():
            current = (meal.image_url or "").strip().lower()
            if (not current) or any(host in current for host in random_hosts):
                meal.image_url = self._default_image(meal.name, "meal")
                meal.save(update_fields=["image_url"])
                meal_fixed += 1

        exercise_fixed = 0
        for exercise in ExercisePlan.objects.all():
            current = (exercise.image_url or "").strip().lower()
            if (not current) or any(host in current for host in random_hosts):
                exercise.image_url = self._default_image(exercise.name, "exercise")
                exercise.save(update_fields=["image_url"])
                exercise_fixed += 1

        self.stdout.write(self.style.SUCCESS(
            f"Image URL repair complete. meals_fixed={meal_fixed}, exercises_fixed={exercise_fixed}"
        ))
