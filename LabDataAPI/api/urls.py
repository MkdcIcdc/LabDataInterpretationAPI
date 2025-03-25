from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PatientDataViewSet

router = DefaultRouter()
router.register(r"patient-data", PatientDataViewSet, basename="patient-data")

urlpatterns = router.urls
