from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from .exceptions import FileUploadError, CustomFileNotFoundError
import logging

logger = logging.getLogger(__name__)


class CustomExceptionMiddleware:
    def __init__(self, get_response):
        logger.debug("Middleware initialized")
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(request, exception):
        logger.debug(f"Exception caught: {exception}")

        if isinstance(exception, ValidationError):
            return JsonResponse(data={'error': 'Validation Error', 'details': exception.detail}, status=400)

        if isinstance(exception, FileUploadError):
            return JsonResponse(data={'error': 'File Upload Error', 'detail': str(exception)},
                                status=exception.status_code)

        if isinstance(exception, CustomFileNotFoundError):
            return JsonResponse(data={'error': 'File Not Found', 'detail': str(exception)},
                                status=exception.status_code)

        if isinstance(exception, ValueError):
            return JsonResponse(data={'error': 'Value Error', 'detail': str(exception)}, status=500)
