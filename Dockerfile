# Используем официальный образ Python версии 3.11
FROM python:3.11

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Копируем файл requirements.txt из локальной директории в контейнер
COPY requirements.txt .

# Устанавливаем необходимые зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы и директории из локальной директории в контейнер
COPY . .

# Задаем команду для выполнения при запуске контейнера: запуск Gunicorn для приложения
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
