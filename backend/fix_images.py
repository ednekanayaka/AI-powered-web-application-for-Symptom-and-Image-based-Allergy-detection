import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import MealPlan

# Mapping for variety
image_map = {
    "Breakfast": "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=600&q=80",
    "Lunch": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
    "Dinner": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=600&q=80"
}

# Specific mappings for variety
specific_images = {
    "Oatmeal": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=600&q=80",
    "Yogurt": "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=600&q=80",
    "Salad": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
    "Steak": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092?auto=format&fit=crop&w=600&q=80",
    "Chicken": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=600&q=80",
    "Fish": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80",
    "Fruit": "https://images.unsplash.com/photo-1494597564530-871f2b93ac55?auto=format&fit=crop&w=600&q=80",
}

for m in MealPlan.objects.all():
    updated = False
    
    # Update if it was a source.unsplash link
    if "source.unsplash.com" in str(m.image_url) or not m.image_url:
        # Try specific keywords first
        for kw, url in specific_images.items():
            if kw.lower() in m.name.lower():
                m.image_url = url
                updated = True
                break
        
        # Fallback to meal type
        if not updated:
            m.image_url = image_map.get(m.meal_type, image_map["Lunch"])
            updated = True
            
        m.save()
        print(f"Fixed image for: {m.name}")

print("Image fix complete!")
