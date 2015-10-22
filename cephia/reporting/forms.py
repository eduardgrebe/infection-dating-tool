from django import forms
from reporting.models import Report

class VisitReportFilterForm(forms.Form):

    visit_date = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(VisitReportFilterForm, self).__init__(*args, **kwargs)
        self.fields['visit_date'].widget = forms.DateInput()
        self.fields['visit_date'].widget.attrs.update({'class':'datepicker'})


class GenericReportFilterForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name','description', 'query']
    def __init__(self, *args, **kwargs):
        super(GenericReportFilterForm, self).__init__(*args, **kwargs)
        
