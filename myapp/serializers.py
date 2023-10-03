from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели File.
    """

    class Meta:
        model = File
        fields = ('file', 'uploaded_at', 'processed')
