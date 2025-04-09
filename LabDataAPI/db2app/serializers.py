from rest_framework import serializers
from .models import MedstatData


class MedstatDataSerializer(serializers.Serializer):
    history_number = serializers.CharField(required=True)


# class MedstatRequestSerializer(serializers.Serializer):
#     """ Сериализатор для валидации входного параметра """
#     research_key = serializers.CharField(max_length=100, required=True)
