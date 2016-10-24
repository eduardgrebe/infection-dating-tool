from user_management.forms import UserCreationForm
from django import forms
from django.forms import formset_factory
from django.forms import ModelForm
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from cephia.models import FileInfo
from django.forms import modelformset_factory
from models import Study, TestPropertyMapping, OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate

class EddiUserCreationForm(UserCreationForm):
    
    def save(self, commit=True):
        
        user = super(EddiUserCreationForm, self).save(True)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.save()
        outside_eddi_group = Group.objects.get(name='Outside Eddi Users')
        outside_eddi_group.user_set.add(user)
        return user

class TestHistoryFileUploadForm(ModelForm):
    class Meta:
        model = FileInfo
        fields = ['data_file']

class StudyForm(ModelForm):
    class Meta:
        model = Study
        fields = ['name']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(StudyForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        studies = Study.objects.filter(user=self.user, name=name)

        if self.instance and self.instance.pk:
            studies = studies.exclude(pk=self.instance.pk)

        if studies.exists():
            raise forms.ValidationError(u"You already created a study with the name %s." % name)
        return name
        
    def save(self, user, commit=True):
        
        study = super(StudyForm, self).save(False)
        study.user = user
        study.save()
        
        return study

class TestPropertyMappingForm(ModelForm):
    test = forms.ModelChoiceField(queryset=OutsideEddiDiagnosticTest.objects.all(), empty_label="(select test)")
    # test_property = forms.ModelChoiceField(queryset=OutsideEddiTestPropertyEstimate.objects.all(), empty_label="(select property)")
    
    class Meta:
        model = TestPropertyMapping
        fields = ['code', 'test']

    def __init__(self, *args, **kwargs):
        super(TestPropertyMappingForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['code'].widget.attrs['readonly'] = True

class OutsideEddiTestPropertyEstimateForm(ModelForm):
    active_property = forms.BooleanField(label="", required=False)
    class Meta:
        fields = (
            'active_property', 'estimate_label',
            'mean_diagnostic_delay_days',
            'foursigma_diagnostic_delay_days', 'diagnostic_delay_median',
            'comment', 'reference'
        )
        model = OutsideEddiTestPropertyEstimate

    def __init__(self, *args, **kwargs):
        super(OutsideEddiTestPropertyEstimateForm, self).__init__(*args, **kwargs)
        if self.instance.pk and not self.instance.user:
            self.fields['estimate_label'].widget.attrs['readonly'] = True
            self.fields['mean_diagnostic_delay_days'].widget.attrs['readonly'] = True
            self.fields['foursigma_diagnostic_delay_days'].widget.attrs['readonly'] = True
            self.fields['diagnostic_delay_median'].widget.attrs['readonly'] = True
            self.fields['comment'].widget.attrs['readonly'] = True
            self.fields['reference'].widget.attrs['readonly'] = True

        self.fields['estimate_label'].widget.attrs['placeholder'] = ''
        self.fields['mean_diagnostic_delay_days'].widget.attrs['placeholder'] = ''
        self.fields['foursigma_diagnostic_delay_days'].widget.attrs['placeholder'] = ''
        self.fields['diagnostic_delay_median'].widget.attrs['placeholder'] = ''
        self.fields['comment'].widget.attrs['placeholder'] = ''
        self.fields['reference'].widget.attrs['placeholder'] = ''
        
        

TestPropertyMappingFormSet = modelformset_factory(
    TestPropertyMapping,
    form=TestPropertyMappingForm
)

TestPropertyEstimateFormSet = modelformset_factory(
    OutsideEddiTestPropertyEstimate,
    form=OutsideEddiTestPropertyEstimateForm
)
    
