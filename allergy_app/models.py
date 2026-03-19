from django.db import models


class Symptom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Symptom"
        verbose_name_plural = "Symptoms"

    def __str__(self):
        return self.name


class Allergy(models.Model):
    name = models.CharField(max_length=100)
    cause = models.TextField()

    class Meta:
        verbose_name = "Allergy"
        verbose_name_plural = "Allergies"

    def __str__(self):
        return self.name


class AllergyRecord(models.Model):
    patient_name = models.CharField(max_length=100)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptom)
    detected_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Allergy Record"
        verbose_name_plural = "Allergy Records"

    def __str__(self):
        return self.patient_name
 