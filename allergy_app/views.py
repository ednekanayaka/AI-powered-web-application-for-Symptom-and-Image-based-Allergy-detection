# allergy_app/views.py
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Symptom, Allergy, AllergyRecord
from .serializers import SymptomSerializer, AllergySerializer, AllergyRecordSerializer

# -------------------------------
# Homepage view
# -------------------------------
def home(request):
    return HttpResponse("Welcome to the Allergy Detection Project!")
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

# -------------------------------
# API ViewSets
# -------------------------------
class SymptomViewSet(viewsets.ModelViewSet):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer

class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer

class AllergyRecordViewSet(viewsets.ModelViewSet):
    queryset = AllergyRecord.objects.all()
    serializer_class = AllergyRecordSerializer
