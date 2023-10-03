from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from .models import File
from .serializers import FileSerializer
from .tasks import process_file
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.exceptions import APIException


@api_view(['POST'])
def upload_file(request: Request) -> Response:
    """
    Эндпоинт для загрузки файла.
    """
    try:
        if request.method == 'POST':
            file_serializer = FileSerializer(data=request.data)
            if file_serializer.is_valid():
                file_obj = file_serializer.save()
                process_file.delay(file_obj.id)
                return Response(file_serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class FileList(ListCreateAPIView):
    """
    API для получения списка файлов.
    """
    serializer_class = FileSerializer

    def get_queryset(self):
        try:
            return File.objects.all()
        except Exception as e:
            raise APIException(str(e))
