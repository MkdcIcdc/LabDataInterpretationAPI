import random
import json
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from api.models import Patient, PatientData
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Генерация тестовых данных PatientData"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Количество записей')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        patients = list(Patient.objects.all())

        if not patients:
            self.stdout.write("❌ Нет пациентов в базе. Создайте их сначала!")
            return

        self.stdout.write(f"📌 Начинаем создание {count} записей PatientData...")

        for _ in range(count):
            patient = random.choice(patients)
            data = {
                "blood_pressure": fake.random_int(min=90, max=180),
                "heart_rate": fake.random_int(min=50, max=120),
                "oxygen_saturation": fake.random_int(min=85, max=100),
                "temperature": round(random.uniform(36.0, 40.0), 1),
                "recorded_at": str(datetime.now() - timedelta(days=random.randint(0, 30))),
            }
            PatientData.objects.create(
                patient=patient,
                medical_data=json.dumps(data),
                created_at=datetime.now()
            )
            self.stdout.write(f"Созданы данные для пациента {patient.full_name} ({patient.id})")

        self.stdout.write("Генерация завершена!")
