from django import forms
from models import FileInfo

class FileInfoForm(forms.ModelForm):

    FILE_TYPE_CHOICES = (
        ('subject','Subject'),
        ('visit','Visit'),
        ('transfer_in','Transfer In'),
        ('transfer_out','Transfer Out'),
        ('annihilation','Annihilation')
    )
    
    class Meta:
        model = FileInfo
        fields = ['data_file','file_type', 'priority']
        widgets = {
            'data_file': forms.FileInput(attrs={'accept':'.xls, .xlsx, .csv'}),
            'priority':forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(FileInfoForm, self).__init__(*args, **kwargs)
        
        for key in self.fields:
            self.fields[key].required = True
        

