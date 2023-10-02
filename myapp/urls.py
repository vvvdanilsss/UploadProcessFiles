from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='file-upload'),
    path('files/', views.FileList.as_view(), name='file-list'),
]
