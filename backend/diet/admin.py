from django.contrib import admin
from .models import Diet

@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'calories', 'date_consumed')
