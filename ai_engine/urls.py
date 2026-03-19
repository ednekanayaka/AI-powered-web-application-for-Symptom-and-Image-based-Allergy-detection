from django.urls import path
from .views import predict_allergy, PredictImageAllergyView

urlpatterns = [
    path("predict/", predict_allergy),
    path("predict-image/", PredictImageAllergyView.as_view()),
]