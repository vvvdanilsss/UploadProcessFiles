from celery import shared_task
from .models import File


@shared_task
def process_file(file_id):
    file_obj = File.objects.get(id=file_id)
    file_path = file_obj.file.path  # Путь к загруженному файлу на сервере

    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:  # Используйте нужную кодировку и опцию errors
            lines = f.readlines()
    except UnicodeDecodeError:
        # Логирование ошибки или другие действия
        return

    line_count = len(lines)

    file_obj.processed = True
    file_obj.metadata = {'line_count': line_count}
    file_obj.save()

