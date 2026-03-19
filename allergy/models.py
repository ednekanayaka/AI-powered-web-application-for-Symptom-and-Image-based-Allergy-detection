from django.db import models
from users.models import UserProfile

class AllergyRecord(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    allergen = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.allergen}"

class AllergyImage(models.Model):
    record = models.ForeignKey(AllergyRecord, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='allergy_images/')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Image for {self.record}"
