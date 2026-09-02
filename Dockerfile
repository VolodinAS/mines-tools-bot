FROM python:3.12-slim

WORKDIR /app

# ВАЖНО: Обновляем корневые сертификаты в минималистичном образе
RUN apt-get update && apt-get install -y ca-certificates && update-ca-certificates && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без создания виртуального окружения
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем исходный код
COPY . .

# Создаём директорию для данных
RUN mkdir -p /app/data

CMD ["python", "-m", "app.bot"]