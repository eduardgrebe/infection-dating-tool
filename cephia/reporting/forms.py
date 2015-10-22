class VisitFilterForm(forms.Form):

    visit_date = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(VisitFilterForm, self).__init__(*args, **kwargs)
        self.fields['visit_date'].widget = forms.DateInput()
        self.fields['visit_date'].widget.attrs.update({'class':'datepicker'})

    def filter(self, visits):
        visit_date = self.cleaned_data['visit_date']
        
        if visit_date:
            visits = visits.filter(visit_date=visit_date)

        return visits
        #visits = visits.exclude(subject__isnull=True)
