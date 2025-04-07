from django.db import models
import uuid


class MedstatData(models.Model):

    
    """ Модель для хранения данных из БД """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    research_key = models.CharField(max_length=100, unique=True) #SQL KEY_RESEARCH
    history_number = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    # first_name = models.CharField(max_length=100)
    # middle_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    patient_result = models.JSONField() #SQL RESULTFORMZAKL
    gender = models.CharField(max_length=10) #SQL SEX
    research_date = models.CharField(max_length=100) #SQL   RESEARCHTIME
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "medstat_data"
        
    def __str__(self):
        return f"{self.fullname} ({self.id})"
    

