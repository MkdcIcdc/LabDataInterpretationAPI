from rest_framework import serializers
from api.models import PatientData, NeuralNetQueue

class PatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientData
        fields = "__all__"

class NeuralNetResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeuralNetQueue
        fields = "__all__"
