from django.db import models


class File(models.Model):
    """
    Модель для хранения информации о загруженных файлах.
    """
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
