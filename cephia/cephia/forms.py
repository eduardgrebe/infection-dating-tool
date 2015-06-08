from django import forms
from models import FileInfo

class FileInfoForm(forms.ModelForm):

    FILE_TYPE_CHOICES = (
        ('subject','Subject'),
        ('visit','Visit')
    )

    class Meta:
        model = FileInfo
        fields = ['data_file','file_type']
        widgets = {
            'data_file': forms.FileInput(),
        }
