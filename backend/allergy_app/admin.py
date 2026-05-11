from django.contrib import admin
from .models import Symptom, Allergy, AllergyRecord

admin.site.register(Symptom)
admin.site.register(Allergy)
admin.site.register(AllergyRecord)
