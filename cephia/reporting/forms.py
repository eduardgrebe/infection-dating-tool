from django import forms

class VisitReportFilterForm(forms.Form):

    visit_date = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(VisitReportFilterForm, self).__init__(*args, **kwargs)
        self.fields['visit_date'].widget = forms.DateInput()
        self.fields['visit_date'].widget.attrs.update({'class':'datepicker'})

    def filter(self, qs_data):
        visit_date = self.cleaned_data['visit_date']
