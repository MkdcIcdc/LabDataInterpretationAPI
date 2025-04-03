from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedstatDataViewSet

router = DefaultRouter()
router.register(r"medstat", MedstatDataViewSet, basename="medstat")

urlpatterns = [
    path("/get-data-from-medstat/", include(router.urls)),
]
