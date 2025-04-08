import time
import requests
from django.utils import timezone
from celery import shared_task
from .models import MedstatData, NeuralNetQueue
from .services.db2_service import load_medstat_data

from celery import shared_task
from .models import MedstatData, NeuralNetQueue, PredictionResult
from .services.db2_service import load_medstat_data
import logging
import uuid

logger = logging.getLogger(__name__)


@shared_task
def orchestrate_data_pipeline(history_number):
    try:
        medstat_data = load_medstat_data(history_number)
        if not medstat_data or not medstat_data.get("researches"):
            logger.warning(f"Нет данных по истории: {history_number}")
            return {"error": "Нет данных"}

        saved_keys = MedstatData.objects.filter(
            history_number=history_number
        ).values_list("research_key", flat=True)

        new_researches = {
            key: val
            for key, val in medstat_data["researches"].items()
            if key not in saved_keys
        }

        if not new_researches:
            logger.info(f"Нет новых исследований для: {history_number}")
            return {"status": "Все исследования уже загружены"}

        for research_key, research_info in new_researches.items():
            MedstatData.objects.create(
                id=uuid.uuid4(),
                fullname=medstat_data["fullname"],
                history_number=history_number,
                research_key=research_key,
                patient_result=research_info["patient_result"],
                gender=medstat_data["gender"],
                research_date=research_info["research_date"],
            )

        last_queue = NeuralNetQueue.objects.order_by("-queue_number").first()
        next_queue_number = (last_queue.queue_number + 1) if last_queue else 1

        queue = NeuralNetQueue.objects.create(
            queue_number=next_queue_number,
            research_key=list(new_researches.keys())[0],  # один для привязки
            history_number=history_number,
        )

        send_patient_data.delay(history_number, queue.queue_number)

        logger.info(f"Поставлена задача на отправку очереди {next_queue_number}")
        return {
            "status": "Данные отправлены в очередь",
            "queue_number": next_queue_number,
        }

    except Exception as e:
        logger.exception(f"Ошибка при постановке задачи: {e}")
        return {"error": str(e)}


@shared_task
def send_patient_data(history_number, queue_number):
    try:
        patient_data = MedstatData.objects.filter(history_number=history_number)

        if not patient_data.exists():
            logger.warning(f"Нет данных для отправки: {history_number}")
            return

        payload = {
            "queue": queue_number,
            "results": [
                {
                    "research_date": item.research_date,
                    "patient_result": item.patient_result,
                }
                for item in patient_data
            ],
        }

        logger.info(f"Отправка данных в нейросеть для очереди {queue_number}")
        response = requests.post("https://example.com/api/predict", json=payload)
        response.raise_for_status()

        time.sleep(30)

        logger.info(f"Запрос результата для очереди {queue_number}")
        result_response = requests.get(f"https://example.com/api/result/{queue_number}")
        result_response.raise_for_status()
        result_data = result_response.json()

        queue = NeuralNetQueue.objects.get(queue_number=queue_number)
        queue.result = result_data
        queue.updated_at = timezone.now()
        queue.save()

        PredictionResult.objects.create(
            queue=queue,
            result_data=result_data,
            history_number=history_number,
            research_key=queue.research_key,
        )

        logger.info(f"Результаты сохранены для очереди {queue_number}")

    except Exception as e:
        logger.exception(f"Ошибка при работе с очередью {queue_number}: {e}")
