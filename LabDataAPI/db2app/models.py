from django.db import models
import uuid


class MedstatData(models.Model):
    """Модель для хранения данных из БД"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    research_key = models.CharField(max_length=100, unique=True)  # SQL KEY_RESEARCH
    history_number = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    patient_result = models.JSONField()  # SQL RESULTFORMZAKL
    gender = models.CharField(max_length=10)  # SQL SEX
    research_date = models.CharField(max_length=100)  # SQL   RESEARCHTIME
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "medstat_data"

    def __str__(self):
        return f"{self.fullname} ({self.id})"


class NeuralNetQueue(models.Model):
    """
    Очередь для запросов к нейросети
    """

    queue_number = models.PositiveIntegerField(unique=True)  # Явное поле номера очереди
    research_key = models.CharField(max_length=100)
    history_number = models.CharField(max_length=100)
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Queue {self.queue_number} - {self.history_number}"


class PredictionResult(models.Model):
    queue = models.OneToOneField(NeuralNetQueue, on_delete=models.CASCADE)
    result_data = models.JSONField()
    research_key = models.CharField(max_length=100)
    history_number = models.CharField(max_length=100)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for Queue {self.queue.queue_number}"
