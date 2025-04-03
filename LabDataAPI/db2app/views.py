from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
import ibm_db
import ibm_db_dbi
import pandas as pd
from .models import MedstatData
from .db2_conn import DB2_DSN
from .serializers import MedstatDataSerializer
from .db2_service import load_medstat_data


class MedstatDataViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"], url_path="load-medstat")
    def load_medstat(self, request, history_number):
        if not history_number:
            return Response({"error": "Параметр 'history_number' обязателен"}, status=status.HTTP_400_BAD_REQUEST)
        medstat_data = load_medstat_data(history_number)
        print(medstat_data)
        if isinstance(medstat_data, dict) and "error" in medstat_data:
            return Response(medstat_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not medstat_data["researches"]:
            return Response({"error": f"Нет данных для истории {history_number}"}, status=status.HTTP_404_NOT_FOUND)
        
        saved_data = []
        for research_key, research_info in medstat_data["researches"].items():
            # Проверяем, есть ли уже такая запись
            if not MedstatData.objects.filter(research_key=research_key).exists():
                medstat_instance = MedstatData(
                    first_name=medstat_data["fullname"].split()[1],
                    middle_name=medstat_data["fullname"].split()[2] if len(medstat_data["fullname"].split()) > 2 else "",
                    last_name=medstat_data["fullname"].split()[0],
                    research_key=research_key,
                    patient_result=research_info["patient_result"],
                    gender=medstat_data["gender"],
                    research_date=research_info["research_date"]
                )
                medstat_instance.save()
                saved_data.append(MedstatDataSerializer(medstat_instance).data)

        return Response(saved_data, status=status.HTTP_201_CREATED)