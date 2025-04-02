from rest_framework import serializers
from .models import MedstatData


class MedstatDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedstatData
        fields = "__all__"
        
# class MedstatRequestSerializer(serializers.Serializer):
#     """ Сериализатор для валидации входного параметра """
#     research_key = serializers.CharField(max_length=100, required=True)
    