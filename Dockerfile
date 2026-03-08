FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем системные зависимости
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Определяем переменные окружения (можно переопределить при запуске)
ENV BOT_TOKEN=""
ENV ADMIN_IDS=""

# Указываем команду для запуска бота
CMD ["python", "bot.py"]

# Порт для доступа к боту (если требуется)
EXPOSE 80