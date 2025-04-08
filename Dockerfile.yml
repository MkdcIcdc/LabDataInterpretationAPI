# Dockerfile
FROM python:3.9-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Команда по умолчанию
CMD ["python", "LabDataAPI/manage.py", "runserver", "0.0.0.0:8004"]
