from django.urls import path
from .views import symptom_prediction

urlpatterns = [
    path("predict-symptom/", symptom_prediction),
]