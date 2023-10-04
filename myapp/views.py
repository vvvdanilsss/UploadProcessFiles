from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from .models import File
from .serializers import FileSerializer
from .tasks import process_file
import logging
from django.db import transaction

logger = logging.getLogger(__name__)


@api_view(['POST'])
def upload_file(request: Request) -> Response:
    """
    Эндпоинт для загрузки файла.
    """
    logger.debug("Function upload_file was called")

    if request.method == 'POST':
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            with transaction.atomic():
                file_obj = file_serializer.save()
                logger.debug(f"File object saved with id={file_obj.id}")
                # Запускаем задачу в Celery после фиксации транзакции
                transaction.on_commit(lambda: process_file.apply_async((file_obj.id,), countdown=5))

            return Response(file_serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=HTTP_400_BAD_REQUEST)


class FileList(ListCreateAPIView):
    """
    API для получения списка файлов.
    """
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.all()
