FROM python:3.12-slim

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости без создания виртуального окружения (оно не нужно в Docker)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем исходный код
COPY . .

# Создаём директорию для данных (если её нет)
RUN mkdir -p /app/data

CMD ["python", "-m", "app.bot"]