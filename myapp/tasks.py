import logging
from typing import Dict, Union
from PIL import Image
from pypdf import PdfReader
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import File

# Настройка логирования
logger = logging.getLogger(__name__)

# Константы для типов файлов
TEXT_FILE_TYPES = ['txt', 'csv']
IMAGE_FILE_TYPES = ['jpg', 'jpeg', 'png']
PDF_FILE_TYPE = 'pdf'


def process_text_file(file_path: str) -> Dict[str, int]:
    """Обработка текстовых файлов."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return {'line_count': len(lines)}


def process_image_file(file_path: str) -> Dict[str, str]:
    """Обработка изображений."""
    with Image.open(file_path) as img:
        img = img.resize((500, 500), Image.LANCZOS)
        img.save(file_path)
    return {'status': 'image resized'}


def process_pdf_file(file_path: str) -> Dict[str, int]:
    """Обработка PDF файлов."""
    pdf_reader = PdfReader(file_path)
    page_count = len(pdf_reader.pages)
    return {'page_count': page_count}


@shared_task(bind=True, max_retries=3)
def process_file(self, file_id: int) -> None:
    """Задача Celery для асинхронной обработки файлов."""
    try:
        # Убран блок with transaction.atomic():
        file_obj = File.objects.get(id=file_id)
        file_path = file_obj.file.path
        file_type = file_path.split('.')[-1]

        metadata: Union[Dict[str, int], Dict[str, str], Dict[str, str]]

        if file_type in TEXT_FILE_TYPES:
            metadata = process_text_file(file_path)

        elif file_type in IMAGE_FILE_TYPES:
            metadata = process_image_file(file_path)

        elif file_type == PDF_FILE_TYPE:
            metadata = process_pdf_file(file_path)

        else:
            metadata = {'status': 'unknown file type'}

        file_obj.processed = True
        file_obj.metadata = metadata
        file_obj.save()
        logger.info(f"Successfully processed file with id {file_id}")

    except ObjectDoesNotExist:
        logger.error(f"File with id {file_id} does not exist")
        # Повторяем задачу с задержкой в 3 секунды
        self.retry(countdown=3, max_retries=3)

    except Exception as e:
        logger.error(f"An unexpected error occurred while processing file with id {file_id}: {str(e)}")
        # Повторяем задачу с задержкой в 5 секунд
        self.retry(countdown=5, max_retries=3)
