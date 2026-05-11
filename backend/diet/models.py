from django.db import models
from users.models import UserProfile

class Diet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    food_item = models.CharField(max_length=255)
    calories = models.PositiveIntegerField()
    date_consumed = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food_item}"
