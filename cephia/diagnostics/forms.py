from django import forms
from cephia.models import Subject, Study, SubjectEDDIStatus

class BaseFilterForm(forms.Form):

    def get_bool(self, value):
        if value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            return None


class SubjectEDDIFilterForm(BaseFilterForm):

    BOOL_CHOICES = (
        ('','---------'),
        (False,'Yes'),
        (True,'No'),
    )

    STATUS_CHOICES = (
        ('','---------'),
        ('ok','OK'),
        ('investigate','Investigate'),
        ('suspected_incorrect_data','Suspected Incorrect Data'),
        ('other','Other'),
    )
    
    subject_label = forms.CharField(max_length=255, required=False)
    source_study = forms.ChoiceField(required=False)
    has_diag_test_history = forms.ChoiceField(choices=BOOL_CHOICES, required=False)
    subject_eddi_status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    
    def __init__(self, *args, **kwargs):
        super(SubjectEDDIFilterForm, self).__init__(*args, **kwargs)

        study_choices = [('','---------')]
        [ study_choices.append((x.id, x.name)) for x in Study.objects.all() ]
        self.fields['source_study'].choices = study_choices

    def filter(self, subjects):
        subject_label = self.cleaned_data['subject_label']
        source_study = self.cleaned_data['source_study']
        has_diag_test_history = self.cleaned_data['has_diag_test_history']
        subject_eddi_status = self.cleaned_data['subject_eddi_status']

        if subject_label:
            subjects = subjects.filter(subject_label=subject_label)
        if source_study:
            subjects = subjects.filter(source_study__id=source_study)
        if has_diag_test_history:
            subjects = subjects.filter(subject_eddi__isnull=self.get_bool(has_diag_test_history))
        if subject_eddi_status:
            subjects = subjects.filter(subject_eddi_status__status=subject_eddi_status)

        return subjects


class SubjectEDDIStatusForm(forms.ModelForm):
    class Meta:
        STATUS_CHOICES = (
            ('ok','OK'),
            ('investigate','Investigate'),
            ('suspected_incorrect_data','Suspected Incorrect Data'),
            ('other','Other'),
        )
        
        model = SubjectEDDIStatus
        fields = ['status', 'comment']
        widgets = {
            'status':forms.Select(choices=STATUS_CHOICES)
        }
    
    def __init__(self, *args, **kwargs):
        super(SubjectEDDIStatusForm, self).__init__(*args, **kwargs)
