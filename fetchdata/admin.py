from django.contrib import admin
from .models import ScraperData, OutputFileUpload, InputFileUpload, ProcessedFile
# Register your models here.

@admin.register(ScraperData)
class ScraperDataAdmin(admin.ModelAdmin):
    list_display = [
        'cryptocurrency',
        'ticker',
        'yesterday_total',
        'today_total',
        'difference',
        'yesterday_icospeaks',
        'today_icospeaks',
        'yesterday_cryptocom',
        'today_cryptocom',
        'yesterday_coinmarket',
        'today_coinmarket',
        'date'
    ]


@admin.register(OutputFileUpload)
class OutputFileUploadAdmin(admin.ModelAdmin):
    list_display = [
        'get_user',
        'file',
        'date_created',
    ]

    def get_user(self, ins):
        input_file = InputFileUpload.get_file_by_output(ins)
        if input_file:
            return input_file.user
        return None

@admin.register(InputFileUpload)
class InputFileUploadAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'input_file',
        'output_file',
        'date_created',
    ]


@admin.register(ProcessedFile)
class ProcessedFileAdmin(admin.ModelAdmin):
    list_display = [
        'get_user',
        'input_file',
        'processed_file',
        'date_created',
    ]

    def get_user(self, ins):
        return ins.input_file.user

