from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('upload-pdf/', views.upload_pdf, name='upload_pdf'),
]
