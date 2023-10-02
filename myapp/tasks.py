from celery import shared_task
from .models import File


@shared_task
def process_file(file_id):
    file_obj = File.objects.get(id=file_id)

    # Здесь будет ваш код для обработки файла
    # ...

    file_obj.processed = True
    file_obj.save()
