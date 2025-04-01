from rest_framework import serializers
from api.models import PatientData, NeuralNetQueue


class MedstatDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedstatData
        fields = "__all__"
        
    research_key = serializers.CharField(max_length=100, unique=True)
    patient_result = serializers.JSONField()
    gender = serializers.CharField(max_length=10)
    research_date = serializers.CharField(max_length=100)    
    created_at = serializers.DateTimeField(auto_now_add=True)
    updated_at = serializers.DateTimeField(auto_now=True)
    
    def create(self, validated_data):
        return MedstatData.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.research_key = validated_data.get('research_key', instance.research_key)
        instance.patient_result = validated_data.get('patient_result', instance.patient_result)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.research_date = validated_data.get('research_date', instance.research_date)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.save()
        return instance
