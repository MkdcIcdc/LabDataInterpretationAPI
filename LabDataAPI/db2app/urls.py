from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoadMedstatAPIView

urlpatterns = [
    path('load-medstat/<str:history_number>/', LoadMedstatAPIView.as_view(), name='load_medstat'),
]