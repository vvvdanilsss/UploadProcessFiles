from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Создаем экземпляр приложения Celery
app = Celery('myproject')

# Используем настройки Django для конфигурации Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover для задач Celery в приложениях
app.autodiscover_tasks()
