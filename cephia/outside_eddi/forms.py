from user_management.forms import UserCreationForm
from django import forms
from django.forms import formset_factory
from django.forms import ModelForm
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import modelformset_factory
from models import Study, TestPropertyMapping, OutsideEddiDiagnosticTest, OutsideEddiTestPropertyEstimate, OutsideEddiFileInfo
from django.db.models import Q

from itertools import groupby
from django.forms.models import ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField

class BaseModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.context = {}
    
    def set_context_data(self, context):
        self.context = context
        return context

    def get_context_data(self, context):
        return self.context

class EddiUserCreationForm(UserCreationForm):
    fields = ['username', 'email']

    def save(self, commit=True):
        
        user = super(EddiUserCreationForm, self).save(True)
        # user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.save()
        outside_eddi_group = Group.objects.get(name='Outside Eddi Users')
        outside_eddi_group.user_set.add(user)
        return user

class TestHistoryFileUploadForm(BaseModelForm):
    class Meta:
        model = OutsideEddiFileInfo
        fields = ['data_file']

        

class StudyForm(BaseModelForm):
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

class TestPropertyMappingForm(BaseModelForm):
    test = forms.ModelChoiceField(queryset=OutsideEddiDiagnosticTest.objects.all(), empty_label=("select test)"))
    
    def clean_code(self):
        code = self.cleaned_data.get('code')

        user = self.context.get('user')

        mappings = TestPropertyMapping.objects.filter(user=user, code=code)

        if self.instance and self.instance.pk:
            mappings = mappings.exclude(pk=self.instance.pk)

        if mappings.exists():
            raise forms.ValidationError('You already have a mapping with the code %s' % code)
        
        return code

    def clean_test_property(self):
        existing = self.cleaned_data['test_property']
        user = self.context['user']

        instance = OutsideEddiTestPropertyEstimate.objects.filter(Q(user__isnull=True) | Q(user=user))

        if existing:
            return instance.filter(pk=existing.pk).first()
        else:
            return None
    
    class Meta:
        model = TestPropertyMapping
        fields = ['code', 'test', 'test_property']
        widgets = {
            'test_property': forms.HiddenInput()
        }

    def save(self, commit=True):
        self.instance.user = self.context['user']
        return super(TestPropertyMappingForm, self).save(commit)
        
        

class OutsideEddiTestPropertyEstimateForm(BaseModelForm):
    active_property = forms.BooleanField(label="", required=False)

    class Meta:
        fields = (
            'is_default', 'estimate_label',
            'mean_diagnostic_delay_days',
            'foursigma_diagnostic_delay_days', 'diagnostic_delay_median',
            'comment', 'reference'
        )
        model = OutsideEddiTestPropertyEstimate
        widgets = {
            'is_default': forms.HiddenInput()
        }

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
        
class GlobalTestForm(BaseModelForm):

    class Meta:
        model = OutsideEddiDiagnosticTest
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(GlobalTestForm, self).__init__(*args, **kwargs)
        if self.instance.pk and not self.instance.user:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['description'].widget.attrs['readonly'] = True

class UserTestForm(BaseModelForm):
    
    class Meta:
        model = OutsideEddiDiagnosticTest
        fields = ['name', 'description']


class UserTestPropertyDefaultForm(forms.Form):
    default_property = forms.ChoiceField(widget=forms.RadioSelect())

    
TestPropertyMappingFormSet = modelformset_factory(
    TestPropertyMapping,
    form=TestPropertyMappingForm,
    extra=0
)

DataFileTestPropertyMappingFormSet = modelformset_factory(
    TestPropertyMapping,
    form=TestPropertyMappingForm,
    extra=0
)

TestPropertyEstimateFormSet = modelformset_factory(
    OutsideEddiTestPropertyEstimate,
    form=OutsideEddiTestPropertyEstimateForm
)

UserTestPropertyEstimateFormSet = modelformset_factory(
    OutsideEddiTestPropertyEstimate,
    form=OutsideEddiTestPropertyEstimateForm
)
    
GlobalTestFormSet = modelformset_factory(
    OutsideEddiDiagnosticTest,
    form=GlobalTestForm,
    extra=0
)

UserTestFormSet = modelformset_factory(
    OutsideEddiDiagnosticTest,
    form=UserTestForm
)

class Grouped(object):
    def __init__(self, queryset, group_by_field,
                 group_label=None, *args, **kwargs):
        """ 
        ``group_by_field`` is the name of a field on the model to use as
                           an optgroup.
        ``group_label`` is a function to return a label for each optgroup.
        """
        super(Grouped, self).__init__(queryset, *args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            
            self.group_label = group_label
   
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset.all()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, choices in groupby(self.queryset.all().order_by('-user', 'name'),
                    key=lambda row: getattr(row, self.field.group_by_field)):
            if not group:
                group = 'Global Tests'
            else:
                group = 'Your Tests'
            if self.field.group_label(group):
                yield (
                    self.field.group_label(group),
                    [self.choice(ch) for ch in choices]
                )


class GroupedModelChoiceField(Grouped, ModelChoiceField):
    choices = property(Grouped._get_choices, ModelChoiceField._set_choices)


class GroupedModelMultiChoiceField(Grouped, ModelMultipleChoiceField):
    choices = property(Grouped._get_choices, ModelMultipleChoiceField._set_choices)
