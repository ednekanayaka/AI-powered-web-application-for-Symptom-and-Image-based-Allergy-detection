# allergy_app/urls.py
from rest_framework import routers
from .views import SymptomViewSet, AllergyViewSet, AllergyRecordViewSet

router = routers.DefaultRouter()
router.register(r'symptoms', SymptomViewSet)
router.register(r'allergies', AllergyViewSet)
router.register(r'allergy-records', AllergyRecordViewSet)

urlpatterns = router.urls
