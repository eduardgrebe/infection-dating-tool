from django import forms
from cephia.models import Subject, Study, SubjectEDDIStatus
from django.db.models import F

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

    INVERTED_CHOICES = (
        ('','---------'),
        (True,'Yes'),
        (False,'No'),
    )

    STATUS_CHOICES = (
        ('','---------'),
        ('ok','OK'),
        ('investigate','Investigate'),
        ('suspected_incorrect_data','Suspected Incorrect Data'),
        ('resolved','Resolved'),
        ('other','Other'),
    )

    EDDI_CHOICES = (
        ('','---------'),
        ('test_history','Diagnostic Test History'),
        ('edsc_adjusted','Reported EDSC (adjusted)'),
    )
    
    subject_label = forms.CharField(max_length=255, required=False)
    source_study = forms.ChoiceField(required=False)
    has_eddi_data = forms.ChoiceField(choices=BOOL_CHOICES, required=False)
    subject_eddi_status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    interval_size_less_than = forms.IntegerField(required=False)
    interval_size_greater_than = forms.IntegerField(required=False)
    inverted_interval = forms.ChoiceField(choices=INVERTED_CHOICES, required=False)
    eddi_type = forms.ChoiceField(choices=EDDI_CHOICES, required=False)
    
    def __init__(self, *args, **kwargs):
        super(SubjectEDDIFilterForm, self).__init__(*args, **kwargs)

        study_choices = [('','---------')]
        [ study_choices.append((x.id, x.name)) for x in Study.objects.all() ]
        self.fields['source_study'].choices = study_choices

    def filter(self, subjects):
        subject_label = self.cleaned_data['subject_label']
        source_study = self.cleaned_data['source_study']
        has_eddi_data = self.cleaned_data['has_eddi_data']
        subject_eddi_status = self.cleaned_data['subject_eddi_status']
        interval_size_less_than = self.cleaned_data['interval_size_less_than']
        interval_size_greater_than = self.cleaned_data['interval_size_greater_than']
        inverted_interval = self.cleaned_data['inverted_interval']
        eddi_type = self.cleaned_data['eddi_type']

        if subject_label:
            subjects = subjects.filter(subject_label=subject_label)
        if source_study:
            subjects = subjects.filter(source_study__id=source_study)
        if has_eddi_data:
            subjects = subjects.filter(subject_eddi__isnull=self.get_bool(has_eddi_data))
        if subject_eddi_status:
            subjects = subjects.filter(subject_eddi_status__status=subject_eddi_status)
        if interval_size_less_than:
            subjects = subjects.filter(subject_eddi__interval_size__lte=interval_size_less_than)
        if interval_size_greater_than:
            subjects = subjects.filter(subject_eddi__interval_size__gte=interval_size_greater_than)
        if self.get_bool(inverted_interval):
            subjects = subjects.filter(subject_eddi__ep_ddi__gt=F('subject_eddi__lp_ddi'))
        if eddi_type:
            subjects = subjects.filter(subject_eddi__eddi_type=eddi_type)

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
