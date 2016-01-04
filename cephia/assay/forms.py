from django import forms
from cephia.models import FileInfo, Panels

class PanelCaptureForm(forms.ModelForm):
    class Meta:
        model = Panels
        fields = ['name','description', 'specimen_type', 'volume']
    
    def __init__(self, *args, **kwargs):
        super(PanelCaptureForm, self).__init__(*args, **kwargs)


class PanelFileForm(forms.ModelForm):
    class Meta:
        model = FileInfo
        fields = ['data_file','file_type', 'priority']
        widgets = {
            'data_file': forms.FileInput(attrs={'accept':'.xls, .xlsx, .csv'}),
            'priority':forms.HiddenInput(),
            'file_type':forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(PanelFileForm, self).__init__(*args, **kwargs)
        
        for key in self.fields:
            self.fields[key].required = True
