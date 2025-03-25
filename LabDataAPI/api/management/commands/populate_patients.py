import random
from django.core.management.base import BaseCommand
from api.models import Patient
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = "Заполняет базу данных случайными пациентами"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Количество пациентов для генерации')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        patients = []

        for _ in range(count):
            patient = Patient(
                full_name=fake.name(),
                gender=random.choice(['M', 'F']),
                lotus_id=fake.ssn(),
            )
            patients.append(patient)

        Patient.objects.bulk_create(patients)  # Массовое создание записей
        self.stdout.write(self.style.SUCCESS(f'Успешно добавлено {count} пациентов'))