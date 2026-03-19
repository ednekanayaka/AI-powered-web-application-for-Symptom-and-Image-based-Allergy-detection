from django.db import models
from users.models import UserProfile

class Exercise(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField()
    date_done = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity}"
