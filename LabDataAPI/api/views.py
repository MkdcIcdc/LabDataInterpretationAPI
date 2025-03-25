from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import PatientData, NeuralNetQueue
from .serializers import PatientDataSerializer, NeuralNetResultSerializer
from .tasks import send_to_neural_network

class PatientDataViewSet(viewsets.ViewSet):
    """
    API для работы с медицинскими данными пациентов и нейросетью.
    """

    @action(detail=True, methods=["get"])
    def get_patient_data(self, request, pk=None):
        """
        Получает медицинские данные пациента по ID пациента.
        """
        patient_data = get_object_or_404(PatientData, patient_id=pk)
        serializer = PatientDataSerializer(patient_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def send_to_neural_network(self, request, pk=None):
        """
        Отправляет медицинские данные пациента в нейросеть.
        """
        patient_data = get_object_or_404(PatientData, patient_id=pk)
        task = send_to_neural_network.delay(patient_data.id)  # Запускаем задачу Celery
        return Response({"task_id": task.id, "message": "Data sent to neural network"}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["get"])
    def get_neural_result(self, request, pk=None):
        """
        Получает результат от нейросети по номеру очереди.
        """
        result = get_object_or_404(NeuralNetResult, patient_data_id=pk)
        serializer = NeuralNetResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)
