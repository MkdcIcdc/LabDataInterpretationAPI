import time
import random
from celery import shared_task
from .models import PatientData, NeuralNetQueue

@shared_task
def send_to_neural_network(patient_data_id):
    """
    Отправляет данные пациента в нейросеть, ждет ответа и сохраняет результат.
    """
    try:
        # Имитируем отправку данных
        patient_data = PatientData.objects.get(id=patient_data_id)
        queue_id = random.randint(1000, 9999)  # Генерируем номер очереди

        # Ждем 2 минуты (или используем реальный запрос)
        time.sleep(120)

        # Имитируем ответ нейросети
        result = {
            "risk_level": random.choice(["low", "medium", "high"]),
            "recommended_action": random.choice(["monitor", "consult doctor", "emergency"]),
        }

        # Сохраняем результат
        NeuralNetQueue.objects.create(
            patient_data=patient_data,
            queue_id=queue_id,
            result_data=result,
        )

        return {"queue_id": queue_id, "status": "completed"}
    except Exception as e:
        return {"error": str(e)}
