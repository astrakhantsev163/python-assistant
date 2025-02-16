# Шаг 1: Используем официальный образ Python как базовый
FROM python:3.11-slim

# Шаг 2: Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Шаг 3: Создаем рабочую директорию внутри контейнера
WORKDIR /

# Шаг 4: Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Шаг 5: Копируем остальные файлы проекта
COPY . .

# Шаг 6: Экспортируем переменные окружения (если они нужны)
ENV PYTHONPATH=/

# Шаг 7: Открываем порт 8000 для FastAPI
EXPOSE 8000

# Шаг 8: Запускаем приложение через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]