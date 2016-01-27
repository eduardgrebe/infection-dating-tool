from django import forms
from cephia.models import Subject, Study

class BaseFilterForm(forms.Form):

    def get_bool(self, value):
        if value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            return None


class SubjectEDDIFilterForm(BaseFilterForm):

    subject_label = forms.CharField(max_length=255, required=False)
    source_study = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super(SubjectEDDIFilterForm, self).__init__(*args, **kwargs)

        study_choices = [('','---------')]
        [ study_choices.append((x.id, x.name)) for x in Study.objects.all() ]
        self.fields['source_study'].choices = study_choices

    def filter(self, subjects):
        subject_label = self.cleaned_data['subject_label']
        source_study = self.cleaned_data['source_study']

        if subject_label:
            subjects = subjects.filter(subject_label=subject_label)
        if source_study:
            subjects = subjects.filter(source_study__id=source_study)

        return subjects
