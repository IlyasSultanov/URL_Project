# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создаем и переходим в рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости проекта
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем весь проект
COPY . .

# Команда для запуска (измените на свою, если нужно)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.wsgi:application"]
