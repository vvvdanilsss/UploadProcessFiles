import pytest
from django.urls import reverse
from rest_framework import status

from myapp.exceptions import FileUploadError
from myapp.models import File
from django.core.files.uploadedfile import SimpleUploadedFile

from myapp.tasks import process_file
from unittest.mock import patch


# Тест для проверки успешной загрузки файла
@pytest.mark.django_db
def test_file_upload_success(client):
    url = reverse('file-upload')
    data = {'file': SimpleUploadedFile("file.txt", b"file_content")}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert File.objects.count() == 1


# Тест для проверки неудачной загрузки файла (неверный формат данных)
@pytest.mark.django_db
def test_file_upload_bad_request(client):
    url = reverse('file-upload')
    data = {'wrong_field': 'wrong_value'}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# Тест для проверки списка файлов
@pytest.mark.django_db
def test_file_list_success(client):
    url = reverse('file-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


# Тест для проверки Celery задачи
@pytest.mark.django_db
def test_process_file():
    file = File.objects.create(
        file=SimpleUploadedFile("file.txt", b"file_content"),
        uploaded_at="2022-01-01T12:00",
        processed=False
    )
    process_file(file.id)
    file.refresh_from_db()
    assert file.processed is True


# Тест для проверки обработки неизвестного типа файла
@pytest.mark.django_db
def test_process_file_unknown_type():
    file = File.objects.create(
        file=SimpleUploadedFile("file.unknown", b"file_content"),
        uploaded_at="2022-01-01T12:00",
        processed=False
    )
    process_file(file.id)
    file.refresh_from_db()
    assert file.processed is True


# Тест для проверки обработки исключений во views
@pytest.mark.django_db
def test_file_upload_server_error(client, monkeypatch):
    def mock_raise(*args, **kwargs):
        raise ValueError("Тестовая ошибка")

    monkeypatch.setattr("myapp.serializers.FileSerializer.is_valid", mock_raise)

    url = reverse('file-upload')
    data = {'file': SimpleUploadedFile("file.txt", b"file_content")}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {'error': 'Value Error', 'detail': 'Тестовая ошибка'}
