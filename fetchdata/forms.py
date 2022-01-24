from django import forms
from .models import OutputFileUpload, InputFileUpload

class OutputFileUploadForm(forms.ModelForm):
    class Meta:
        model = OutputFileUpload
        fields = [
            "file",
        ]

class InputFileUploadForm(forms.ModelForm):
    class Meta:
        model = InputFileUpload
        fields = [
            "input_file",
        ]