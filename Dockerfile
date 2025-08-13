# Используем официальный образ Python 3.12
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем переменные окружения
ENV OPENROUTER_KEY="ключ для openrouter.ai"
ENV MODEL="google/gemma-3-27b-it:free"
ENV URL_ROUTER = "https://openrouter.ai/api/v1/chat/completions"
ENV SECRET_KEY="ключ для кодирования jwt токенов"
ENV ALGORITHM="HS256"


# Открываем порт для FastAPI
EXPOSE 8000

# Команда для запуска FastAPI и arq воркера
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & arq func.generate_story.WorkerSettings"]