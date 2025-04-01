from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import MedstatData
from .serializers import MedstatDataSerializer


class MedstatDataViewSet(viewsets.ModelViewSet):
    
    @action(detail=True, methods=["get"])
    def get_patient_from_medstat(self, request, pk=None):
        pass
    pass
