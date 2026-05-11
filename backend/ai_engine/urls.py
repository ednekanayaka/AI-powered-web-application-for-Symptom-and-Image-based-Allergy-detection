from django.urls import path
from .views import predict_allergy

urlpatterns = [

    # ✅ FINAL AI ALLERGY API (Symptom + Image)
    path('predict/', predict_allergy, name='predict_allergy'),

]