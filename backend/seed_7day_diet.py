import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import MealPlan

def seed_diet_plans():
    # 1. Clear existing data
    MealPlan.objects.all().delete()
    print("Cleared existing meal plans.")

    plans = []

    # =========================================
    # 🥗 WEIGHT LOSS (lose)
    # =========================================
    lose_data = [
        # Day 1
        ("Breakfast", 1, "Oats with low-fat milk", 250, "10g", "https://images.unsplash.com/photo-1517673132405-a56a62b18caf"),
        ("Lunch", 1, "Brown rice + grilled chicken + mixed vegetables", 500, "35g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
        ("Dinner", 1, "Vegetable soup + salad", 200, "5g", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd"),
        # Day 2
        ("Breakfast", 2, "2 boiled eggs + whole wheat toast", 300, "15g", "https://images.unsplash.com/photo-1525351484163-7529414344d8"),
        ("Lunch", 2, "Brown rice + dhal curry + vegetables", 450, "12g", "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"),
        ("Dinner", 2, "Grilled fish + steamed broccoli", 350, "30g", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2"),
        # Day 3
        ("Breakfast", 3, "Yogurt + banana", 200, "8g", "https://images.unsplash.com/photo-1488477181946-6428a0291777"),
        ("Lunch", 3, "Quinoa + vegetable curry", 400, "10g", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd"),
        ("Dinner", 3, "Chicken salad", 350, "25g", "https://images.unsplash.com/photo-1532550907401-a500c9a57435"),
        # Day 4
        ("Breakfast", 4, "Oatmeal + apple", 280, "8g", "https://images.unsplash.com/photo-1517673132405-a56a62b18caf"),
        ("Lunch", 4, "Brown rice + fish curry", 450, "25g", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2"),
        ("Dinner", 4, "Vegetable soup", 180, "5g", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd"),
        # Day 5
        ("Breakfast", 5, "Smoothie (banana + low-fat milk)", 220, "10g", "https://images.unsplash.com/photo-1502741224143-90386d7f8c82"),
        ("Lunch", 5, "Rice + chicken curry (small portion)", 500, "30g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
        ("Dinner", 5, "Mixed vegetable salad", 150, "5g", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd"),
        # Day 6
        ("Breakfast", 6, "Whole wheat toast + peanut butter", 350, "12g", "https://images.unsplash.com/photo-1509440159596-0249088772ff"),
        ("Lunch", 6, "Brown rice + vegetable curry", 400, "10g", "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"),
        ("Dinner", 6, "Grilled chicken + vegetables", 400, "35g", "https://images.unsplash.com/photo-1532550907401-a500c9a57435"),
        # Day 7
        ("Breakfast", 7, "Yogurt + fruits", 180, "8g", "https://images.unsplash.com/photo-1488477181946-6428a0291777"),
        ("Lunch", 7, "Rice + dhal + vegetables", 450, "12g", "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"),
        ("Dinner", 7, "Vegetable soup", 180, "5g", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd"),
    ]
    for m in lose_data:
        plans.append(MealPlan(goal_type="lose", meal_type=m[0], day=m[1], name=m[2], calories=m[3], protein=m[4], image_url=m[5]))

    # =========================================
    # 🍛 WEIGHT GAIN (gain)
    # =========================================
    gain_data = [
        # Day 1
        ("Breakfast", 1, "Milk + banana + 2 eggs", 550, "25g", "https://images.unsplash.com/photo-1525351484163-7529414344d8"),
        ("Lunch", 1, "Rice + chicken curry + dhal", 800, "40g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
        ("Dinner", 1, "Rice + fish curry", 700, "35g", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2"),
        # Day 2
        ("Breakfast", 2, "Oats with milk + nuts", 600, "20g", "https://images.unsplash.com/photo-1517673132405-a56a62b18caf"),
        ("Lunch", 2, "Rice + beef curry", 850, "45g", "https://images.unsplash.com/photo-1600891964599-f61ba0e24092"),
        ("Dinner", 2, "Pasta + vegetables", 750, "20g", "https://images.unsplash.com/photo-1473093226795-af9932fe5856"),
        # Day 3
        ("Breakfast", 3, "Bread + butter + eggs", 500, "20g", "https://images.unsplash.com/photo-1509440159596-0249088772ff"),
        ("Lunch", 3, "Rice + chicken curry", 750, "40g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
        ("Dinner", 3, "Rice + dhal curry", 650, "15g", "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"),
        # Day 4
        ("Breakfast", 4, "Peanut butter toast + milk", 550, "18g", "https://images.unsplash.com/photo-1509440159596-0249088772ff"),
        ("Lunch", 4, "Rice + fish curry", 750, "35g", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2"),
        ("Dinner", 4, "Fried rice with egg", 800, "25g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
        # Day 5
        ("Breakfast", 5, "Pancakes + milk", 600, "15g", "https://images.unsplash.com/photo-1528207776546-365bb710ee93"),
        ("Lunch", 5, "Rice + meat curry", 850, "45g", "https://images.unsplash.com/photo-1600891964599-f61ba0e24092"),
        ("Dinner", 5, "Pasta + chicken", 800, "40g", "https://images.unsplash.com/photo-1473093226795-af9932fe5856"),
        # Day 6
        ("Breakfast", 6, "Oats + milk", 450, "15g", "https://images.unsplash.com/photo-1517673132405-a56a62b18caf"),
        ("Lunch", 6, "Rice + chicken curry", 750, "40g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
        ("Dinner", 6, "Rice + egg curry", 650, "20g", "https://images.unsplash.com/photo-1525351484163-7529414344d8"),
        # Day 7
        ("Breakfast", 7, "Smoothie + bread", 500, "15g", "https://images.unsplash.com/photo-1502741224143-90386d7f8c82"),
        ("Lunch", 7, "Rice + fish curry", 750, "35g", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2"),
        ("Dinner", 7, "Rice + dhal curry", 650, "15g", "https://images.unsplash.com/photo-1546069901-ba9599a7e63c"),
    ]
    for m in gain_data:
        plans.append(MealPlan(goal_type="gain", meal_type=m[0], day=m[1], name=m[2], calories=m[3], protein=m[4], image_url=m[5]))

    # =========================================
    # 💪 MUSCLE GAIN (muscle)
    # =========================================
    muscle_data = [
        # Day 1
        ("Breakfast", 1, "3 boiled eggs + oats", 500, "30g", "https://images.unsplash.com/photo-1525351484163-7529414344d8"),
        ("Lunch", 1, "Chicken breast + brown rice", 700, "50g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
        ("Dinner", 1, "Grilled fish + vegetables", 550, "40g", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2"),
        # Day 2
        ("Breakfast", 2, "Peanut butter toast + milk", 500, "20g", "https://images.unsplash.com/photo-1509440159596-0249088772ff"),
        ("Lunch", 2, "Beef curry + rice", 800, "45g", "https://images.unsplash.com/photo-1600891964599-f61ba0e24092"),
        ("Dinner", 2, "Chicken salad", 600, "40g", "https://images.unsplash.com/photo-1532550907401-a500c9a57435"),
        # Day 3
        ("Breakfast", 3, "Oats + eggs", 450, "25g", "https://images.unsplash.com/photo-1517673132405-a56a62b18caf"),
        ("Lunch", 3, "Fish + rice", 650, "40g", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2"),
        ("Dinner", 3, "Chicken breast + vegetables", 600, "50g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
        # Day 4
        ("Breakfast", 4, "Eggs + milk", 400, "25g", "https://images.unsplash.com/photo-1525351484163-7529414344d8"),
        ("Lunch", 4, "Chicken pasta", 750, "45g", "https://images.unsplash.com/photo-1473093226795-af9932fe5856"),
        ("Dinner", 4, "Tuna salad", 500, "40g", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd"),
        # Day 5
        ("Breakfast", 5, "Oats + banana", 400, "15g", "https://images.unsplash.com/photo-1517673132405-a56a62b18caf"),
        ("Lunch", 5, "Chicken breast + rice", 700, "50g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
        ("Dinner", 5, "Fish curry", 650, "40g", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2"),
        # Day 6
        ("Breakfast", 6, "Eggs + toast", 450, "25g", "https://images.unsplash.com/photo-1525351484163-7529414344d8"),
        ("Lunch", 6, "Beef + rice", 800, "45g", "https://images.unsplash.com/photo-1600891964599-f61ba0e24092"),
        ("Dinner", 6, "Chicken salad", 600, "40g", "https://images.unsplash.com/photo-1532550907401-a500c9a57435"),
        # Day 7
        ("Breakfast", 7, "Oats + milk", 400, "15g", "https://images.unsplash.com/photo-1517673132405-a56a62b18caf"),
        ("Lunch", 7, "Fish + rice", 650, "40g", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2"),
        ("Dinner", 7, "Chicken breast + vegetables", 600, "50g", "https://images.unsplash.com/photo-1512058564366-18510be2db19"),
    ]
    for m in muscle_data:
        plans.append(MealPlan(goal_type="muscle", meal_type=m[0], day=m[1], name=m[2], calories=m[3], protein=m[4], image_url=m[5]))

    # Bulk create
    MealPlan.objects.bulk_create(plans)
    print(f"Successfully seeded {len(plans)} meal records!")

if __name__ == "__main__":
    seed_diet_plans()
