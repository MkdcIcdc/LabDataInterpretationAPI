from django.db import models


class Patient(models.Model):
    """
    Модель для хранения данных пациента
    """
    GENDER_TYPE = (
        ("male", "Мужчина"),
        ("female", "Женщина"),
    )
    
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    lotus_id = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} ({self.id})"
    

class PatientData(models.Model):
    """
    Модель для хранения исходных данных пациента
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="data")
    medical_data = models.JSONField()  # Исходные данные пациента
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Data for Patient {self.patient.id} at {self.recorded_at}"

class NeuralNetQueue(models.Model):
    """
    Модель для хранения очереди запросов к нейросети и результатов обработки запросов
    """
    STATUS_TYPE = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    )
    
    patient_data = models.ForeignKey(PatientData, on_delete=models.CASCADE, related_name="queue")
    status = models.CharField(max_length=20, choices=STATUS_TYPE, default='pending')
    result = models.JSONField(null=True, blank=True)  # Ответ от нейросети
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Queue {self.id} - {self.status}"
    