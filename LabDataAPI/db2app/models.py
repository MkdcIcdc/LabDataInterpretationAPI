from django.db import models


class MedstatData(models.Model):

    
    """ Модель для хранения данных из БД """
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    research_key = models.CharField(max_length=100, unique=True) #SQL KEY_RESEARCH
    patient_result = models.JSONField() #SQL RESULTFORMZAKL
    gender = models.CharField(max_length=10) #SQL SEX
    research_date = models.CharField(max_length=100) #SQL   RESEARCHTIME
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "medstat_data"
        
    def __str__(self):
        return f"{self.fullname} ({self.id})"
    

