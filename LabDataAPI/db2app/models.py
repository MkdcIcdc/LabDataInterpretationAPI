from django.db import models


class DB2Data(models.Model):
    
    """ Модель для хранения данных из БД """
    
    patient_key = models.CharField(max_length=100, unique=True) #SQL KEY
    research_key = models.CharField(max_length=100, unique=True) #SQL KEY_RESEARCH
    fullname = models.CharField(max_length=100) #SQL FIRSTNAME + MIDDLENAME + LASTNAME
    patient_result = models.JSONField() #SQL RESULTFORMZAKL
    gender = models.CharField(max_length=10) #SQL SEX
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = "RESEARCHES"
        app_label = "db2app"
        
    def __str__(self):
        return f"{self.fullname} ({self.id})"
    

