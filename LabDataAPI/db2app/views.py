from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework.response import Response
from rest_framework.views import APIView
from .services.db2_conn import DB2_DSN
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_yasg.utils import swagger_auto_schema

from .tasks import orchestrate_data_pipeline
from .serializers import MedstatDataSerializer

class TriggerPipelineView(APIView):
    @swagger_auto_schema(operation_description="description")
    def post(self, request):
        history_number = request.data.get("history_number")
        if not history_number:
            return Response({"error": "history_number is required"}, status=status.HTTP_400_BAD_REQUEST)

        orchestrate_data_pipeline.delay(history_number)
        return Response({"message": "Pipeline triggered"}, status=status.HTTP_202_ACCEPTED)