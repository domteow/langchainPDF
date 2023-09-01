from django.db import models

# Create your models here.
class UploadedPDF(models.Model):
    file = models.FileField(upload_to='pdfs/')
    timestamp = models.DateTimeField(auto_now_add=True)