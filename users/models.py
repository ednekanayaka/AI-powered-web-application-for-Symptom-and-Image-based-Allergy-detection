from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    # You can add extra fields if needed
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return self.username
