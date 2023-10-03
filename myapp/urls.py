from typing import List
from django.urls import path, URLPattern
from . import views

urlpatterns: List[URLPattern] = [
    path('upload/', views.upload_file, name='file-upload'),
    path('files/', views.FileList.as_view(), name='file-list'),
]
