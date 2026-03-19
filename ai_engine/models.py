from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    symptoms = models.TextField()

    prediction = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction}"