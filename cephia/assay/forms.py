from django import forms
from models import Panel

class PanelCaptureForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['name','description', 'specimen_type', 'volume']
    
    def __init__(self, *args, **kwargs):
        super(PanelCaptureForm, self).__init__(*args, **kwargs)
