from typing import Dict, Union
from PIL import Image
from PyPDF2 import PdfReader
from celery import shared_task
from .models import File

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


@shared_task
def process_file(file_id: int) -> None:
    """Задача Celery для асинхронной обработки файлов."""
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
