from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from .exceptions import FileUploadError, CustomFileNotFoundError


class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(request, exception):
        if isinstance(exception, ValidationError):
            return JsonResponse(data={'error': 'Validation Error', 'details': exception.detail}, status=400)

        if isinstance(exception, FileUploadError):
            return JsonResponse(data={'error': 'File Upload Error', 'detail': str(exception)},
                                status=exception.status_code)

        if isinstance(exception, CustomFileNotFoundError):
            return JsonResponse(data={'error': 'File Not Found', 'detail': str(exception)},
                                status=exception.status_code)
