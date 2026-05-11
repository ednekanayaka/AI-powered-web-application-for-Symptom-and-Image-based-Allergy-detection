import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import MealPlan

new_meals = [
    # MUSCLE GAIN ALTERNATIVES
    {"goal_type": "muscle", "meal_type": "Breakfast", "name": "Greek Yogurt with Berries and Nuts", "calories": 450, "protein": "30g"},
    {"goal_type": "muscle", "meal_type": "Breakfast", "name": "Whole Grain Toast with Avocado and Turkey", "calories": 500, "protein": "25g"},
    {"goal_type": "muscle", "meal_type": "Lunch", "name": "Beef and Broccoli Stir Fry with Brown Rice", "calories": 700, "protein": "45g"},
    {"goal_type": "muscle", "meal_type": "Lunch", "name": "Salmon and Quinoa Power Bowl", "calories": 650, "protein": "40g"},
    {"goal_type": "muscle", "meal_type": "Dinner", "name": "Roasted Turkey Breast with Mashed Potatoes", "calories": 750, "protein": "50g"},
    {"goal_type": "muscle", "meal_type": "Dinner", "name": "Lentil and Tofu Curry with Naan", "calories": 600, "protein": "35g"},

    # WEIGHT LOSS ALTERNATIVES
    {"goal_type": "lose", "meal_type": "Breakfast", "name": "Overnight Oats with Chia Seeds", "calories": 300, "protein": "10g"},
    {"goal_type": "lose", "meal_type": "Breakfast", "name": "Low-Fat Cottage Cheese with Pineapple", "calories": 250, "protein": "20g"},
    {"goal_type": "lose", "meal_type": "Lunch", "name": "Grilled Lemon Herb Chicken Salad", "calories": 350, "protein": "35g"},
    {"goal_type": "lose", "meal_type": "Lunch", "name": "Zucchini Noodles with Pesto and Shrimp", "calories": 320, "protein": "25g"},
    {"goal_type": "lose", "meal_type": "Dinner", "name": "Steamed White Fish with Bok Choy", "calories": 280, "protein": "30g"},
    {"goal_type": "lose", "meal_type": "Dinner", "name": "Vegetable and Bean Soup", "calories": 250, "protein": "15g"},

    # GENERAL HEALTH ALTERNATIVES
    {"goal_type": "general", "meal_type": "Breakfast", "name": "Peanut Butter Banana Toast", "calories": 350, "protein": "12g"},
    {"goal_type": "general", "meal_type": "Breakfast", "name": "Homemade Granola with Almond Milk", "calories": 400, "protein": "10g"},
    {"goal_type": "general", "meal_type": "Lunch", "name": "Mediterranean Chickpea Wrap", "calories": 450, "protein": "15g"},
    {"goal_type": "general", "meal_type": "Lunch", "name": "Turkey and Swiss Sandwich on Whole Wheat", "calories": 500, "protein": "25g"},
    {"goal_type": "general", "meal_type": "Dinner", "name": "Baked Cod with Roasted Vegetables", "calories": 400, "protein": "30g"},
    {"goal_type": "general", "meal_type": "Dinner", "name": "Sweet Potato and Black Bean Tacos", "calories": 450, "protein": "18g"},
]

for meal_data in new_meals:
    # Check if exists to avoid duplicates
    if not MealPlan.objects.filter(name=meal_data["name"]).exists():
        MealPlan.objects.create(
            goal_type=meal_data["goal_type"],
            meal_type=meal_data["meal_type"],
            name=meal_data["name"],
            calories=meal_data["calories"],
            protein=meal_data["protein"],
            image_url=f"https://source.unsplash.com/400x300/?{meal_data['name'].replace(' ', ',')}"
        )

print("Seeding complete!")
