from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import ibm_db
import ibm_db_dbi
import pandas as pd
from .models import MedstatData
from .db2_conn import DB2_DSN
from .serializers import MedstatDataSerializer, MedstatRequestSerializer


class GetPatientFromMedstat(APIView):
    def get(self, request):
        serializer = MedstatRequestSerializer(data=request.query_params)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        research_key = serializer.validated_data["research_key"]
        
        try:
            conn = ibm_db.connect(DB2_DSN, "", "")
            if not conn:
                return Response({"error": "Ошибка подключения к DB2"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            sql_query = f'''
            SELECT 
                r2.KEY_RESEARCH AS research_key, 
                r2.RESULTFORMZAKL AS patient_result, 
                h.SEX AS gender,
                r.RESEARCHTIME AS research_date
            FROM HISTORY h
            LEFT JOIN RESEARCHES r ON r.KEY_HISTORY = h.KEY
            LEFT JOIN RESEARCH_RESULTSR2 r2 ON r.KEY = r2.KEY_RESEARCH
            WHERE r2.KEY_RESEARCH = '{research_key}';
            '''
            
            stmt = ibm_db.exec_immediate(conn, sql_query)
            result = ibm_db.fetch_assoc(stmt)
            ibm_db.close(conn)
            
            if not result:
                return Response({"error": "Данные не найдены"}, status=status.HTTP_404_NOT_FOUND)
            
            # Подготовка данных для сохранения
            data = {
                "research_key": result["RESEARCH_KEY"],
                "patient_result": result["PATIENT_RESULT"],
                "gender": result["GENDER"],
                "research_date": result["RESEARCH_DATE"]
            }
            
            # Сохранение в PostgreSQL
            medstat_serializer = MedstatDataSerializer(data=data)
            if medstat_serializer.is_valid():
                medstat_serializer.save()
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": f"Ошибка при выполнении запроса: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
