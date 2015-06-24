from django import forms
from models import FileInfo

class FileInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FileInfoForm, self).__init__(*args, **kwargs)
        self.fields['data_file'].required = True
        self.fields['file_type'].required = True

    FILE_TYPE_CHOICES = (
        ('subject','Subject'),
        ('visit','Visit'),
        ('transfer_in','Transfer In'),
        ('transfer_out','Transfer Out'),
        ('missing_transfer_out','Missing Transfer Out'),
        ('annihilation','Annihilation')
    )

    class Meta:
        model = FileInfo
        fields = ['data_file','file_type']
        widgets = {
            'data_file': forms.FileInput(),
        }
