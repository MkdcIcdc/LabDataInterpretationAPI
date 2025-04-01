from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MedstatDataViewSet

router = DefaultRouter()
router.register(r"get-medstat-data", MedstatDataViewSet, basename="medstate-data")

urlpatterns = router.urls