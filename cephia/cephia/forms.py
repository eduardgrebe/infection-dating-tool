from django import forms
from models import FileInfo, ImportedRowComment

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
        }
    
    def __init__(self, *args, **kwargs):
        super(FileInfoForm, self).__init__(*args, **kwargs)
        
        for key in self.fields:
            self.fields[key].required = True


class RowCommentForm(forms.ModelForm):
    class Meta:
        ACTION_CHOICES = (
            ('action1','Action1'),
            ('action2', 'Action2'),
        )
        model = ImportedRowComment
        fields = ['resolve_date','resolve_action', 'assigned_to', 'comment']
        widgets = {
            'resolve_date':forms.DateInput(attrs={'class': 'getdadate'}),
            'resolve_action':forms.Select(choices=ACTION_CHOICES)
        }
    
    def __init__(self, *args, **kwargs):
        super(RowCommentForm, self).__init__(*args, **kwargs)
        

