from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GetPatientResultFromMedstat

app_name = "db2app"
urlpatterns = [
    path("get-patient-result-from-medstat/", GetPatientResultFromMedstat.as_view(), name="get-patient-result-from-medstat"),
]
