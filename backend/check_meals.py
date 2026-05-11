import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import MealPlan

for m in MealPlan.objects.all()[:5]:
    print(f"Name: {m.name}, Image: {m.image_url}")
