from django import forms
from reporting.models import Report
from django.conf import settings

class VisitReportFilterForm(forms.Form):

    from_date = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)
    to_date = forms.DateField(required=False, input_formats=settings.DATE_INPUT_FORMATS)

    def __init__(self, *args, **kwargs):
        super(VisitReportFilterForm, self).__init__(*args, **kwargs)
        self.fields['to_date'].widget = forms.DateInput()
        self.fields['to_date'].widget.attrs.update({'class':'datepicker'})
        self.fields['from_date'].widget = forms.DateInput()
        self.fields['from_date'].widget.attrs.update({'class':'datepicker'})


class GenericReportFilterForm(forms.Form):

    query = forms.CharField(required=False, widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super(GenericReportFilterForm, self).__init__(*args, **kwargs)


class GenericReportSaveForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name','description', 'query']
    def __init__(self, *args, **kwargs):
        super(GenericReportSaveForm, self).__init__(*args, **kwargs)
        
