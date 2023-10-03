from rest_framework import status
from rest_framework.exceptions import APIException


class FileUploadError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Ошибка при загрузке файла.'


class CustomFileNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Файл не найден.'
