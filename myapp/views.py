from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import File
from .serializers import FileSerializer
from rest_framework import generics
from .tasks import process_file  # импортируем задачу из Celery

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_obj = file_serializer.save()

            # Здесь вызываем задачу Celery для обработки файла
            process_file.delay(file_obj.id)

            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileList(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
