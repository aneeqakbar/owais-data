import os
from urllib.parse import urlparse
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ScraperData(models.Model):
    SCRAPER_NAMES = (
        ('T', 'Telegram'),
        ('R', 'Reddit'),
    )

    scraper_name = models.CharField(max_length=255, choices=SCRAPER_NAMES)
    cryptocurrency = models.CharField(max_length=255)
    ticker = models.CharField(max_length=50)
    yesterday_total = models.IntegerField(default=0, null=True)
    today_total = models.IntegerField(default=0, null=True)
    difference = models.IntegerField(default=0, null=True)
    yesterday_icospeaks = models.IntegerField(default=0, null=True)
    today_icospeaks = models.IntegerField(default=0, null=True)
    yesterday_cryptocom = models.IntegerField(default=0, null=True)
    today_cryptocom = models.IntegerField(default=0, null=True)
    yesterday_coinmarket = models.IntegerField(default=0, null=True)
    today_coinmarket = models.IntegerField(default=0, null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)

class OutputFileUpload(models.Model):
    file = models.FileField(upload_to='documents/output_files/%Y/%m/%d/')
    date_created = models.DateTimeField(auto_now_add=True)

class InputFileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files_uploaded")
    input_file = models.FileField(upload_to='documents/input_files/%Y/%m/%d/')
    output_file = models.ForeignKey(OutputFileUpload, on_delete=models.CASCADE, related_name="input_files")
    date_created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_file_by_output(output_ins):
        return InputFileUpload.objects.filter(output_file = output_ins).first()

class ProcessedFile(models.Model):
    input_file = models.OneToOneField(InputFileUpload, on_delete=models.CASCADE, related_name="processed_file")
    processed_file = models.FileField(upload_to='documents/processed/%Y/%m/%d/')
    date_created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_files_by_user(user):
        return ProcessedFile.objects.filter(input_file__user = user)

    @property
    def get_name(self):
        return os.path.basename(self.processed_file.url)

    @property
    def get_input_name(self):
        return os.path.basename(self.input_file.input_file.url)

