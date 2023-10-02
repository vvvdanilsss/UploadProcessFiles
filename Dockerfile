# Используйте официальный образ Python
FROM python:3.11

# Установите рабочую директорию в /app
WORKDIR /app

# Скопируйте текущий каталог в /app
COPY . /app

# Установите все необходимые пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Запустите команду при создании контейнера
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
