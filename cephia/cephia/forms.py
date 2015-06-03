from django import forms
from models import FileInfo

class FileInfoForm(forms.ModelForm):
    class Meta:
        model = FileInfo
        fields = ['data_file',]
        widgets = {
            'data_file': forms.FileInput()
        }
