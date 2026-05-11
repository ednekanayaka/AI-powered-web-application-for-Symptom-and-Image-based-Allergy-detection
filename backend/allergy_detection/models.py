from django.db import models


class SymptomReport(models.Model):
    SYMPTOM_CHOICES = [
        ('itching', 'Itching'),
        ('redness', 'Redness'),
        ('swelling', 'Swelling'),
        ('rash', 'Rash'),
        ('sneezing', 'Sneezing'),
        ('runny_nose', 'Runny Nose'),
    ]

    symptom = models.CharField(max_length=50, choices=SYMPTOM_CHOICES)
    severity = models.IntegerField(help_text="1 (low) to 5 (high)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symptom} - {self.severity}"
