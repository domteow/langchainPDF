from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
]
