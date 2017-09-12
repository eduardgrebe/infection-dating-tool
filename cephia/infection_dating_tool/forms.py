from user_management.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group
from django.forms import modelformset_factory, BaseModelFormSet
from models import (
    TestPropertyMapping, IDTDiagnosticTest, IDTTestPropertyEstimate,
    IDTFileInfo, SelectedCategory, GrowthRateEstimate, ResidualRisk,
    VariabilityAdjustment)
from django.db.models import Q
import math
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

class IDTUserCreationForm(UserCreationForm):
    fields = ['username', 'email']

    def save(self, commit=True):

        user = super(IDTUserCreationForm, self).save(True)
        # user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.save()
        idt_group = Group.objects.get_or_create(name='Infection Dating Tool Users')
        idt_group[0].user_set.add(user)
        return user

class TestHistoryFileUploadForm(BaseModelForm):
    class Meta:
        model = IDTFileInfo
        fields = ['data_file']


class TestPropertyMappingForm(BaseModelForm):
    test = forms.ModelChoiceField(queryset=IDTDiagnosticTest.objects.all(), empty_label=("select test)"))

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

        instance = IDTTestPropertyEstimate.objects.filter(Q(user__isnull=True) | Q(user=user))

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



class TestPropertyEstimateForm(BaseModelForm):
    active_property = forms.BooleanField(label="", required=False)

    class Meta:
        fields = (
            'global_default', 'estimate_label',
            'diagnostic_delay', 'detection_threshold',
            'diagnostic_delay_sigma', 'comment'
        )
        model = IDTTestPropertyEstimate
        widgets = {
            'global_default': forms.HiddenInput()
        }

    def __init__(self, test_pk, user, *args, **kwargs):
        super(TestPropertyEstimateForm, self).__init__(*args, **kwargs)
        self.test_pk = test_pk
        test = IDTDiagnosticTest.objects.get(pk=self.test_pk)
        self.user = user
        if self.instance.pk and not self.instance.user:
            self.fields['estimate_label'].widget.attrs['readonly'] = True
            self.fields['diagnostic_delay'].widget.attrs['readonly'] = True
            self.fields['detection_threshold'].widget.attrs['readonly'] = True
            self.fields['foursigma_diagnostic_delay_days'].widget.attrs['readonly'] = True
            self.fields['diagnostic_delay_median'].widget.attrs['readonly'] = True
            self.fields['comment'].widget.attrs['readonly'] = True

        self.fields['estimate_label'].widget.attrs['placeholder'] = ''
        self.fields['diagnostic_delay'].widget.attrs['placeholder'] = ''
        self.fields['detection_threshold'].widget.attrs['placeholder'] = ''
        self.fields['diagnostic_delay_sigma'].widget.attrs['placeholder'] = ''
        self.fields['comment'].widget.attrs['placeholder'] = ''

    def clean_diagnostic_delay(self):
        try:
            test_category = SelectedCategory.objects.get(test__pk=self.test_pk, user=self.user).category
        except SelectedCategory.DoesNotExist:
            test_category = IDTDiagnosticTest.objects.get(pk=self.test_pk).category
        diagnostic_delay = self.cleaned_data['diagnostic_delay']
        if test_category != 'viral_load' and not diagnostic_delay:
            raise forms.ValidationError('This field is required.')
        return diagnostic_delay

    def clean_detection_threshold(self):
        try:
            test_category = SelectedCategory.objects.get(test__pk=self.test_pk, user=self.user).category
        except SelectedCategory.DoesNotExist:
            test_category = IDTDiagnosticTest.objects.get(pk=self.test_pk).category
        detection_threshold = self.cleaned_data['detection_threshold']
        if test_category == 'viral_load' and not detection_threshold:
            raise forms.ValidationError('Viral Load tests must have a detection threshold.')
        return detection_threshold


class TestPropertyEstimateCreateTestForm(BaseModelForm):
    active_property = forms.BooleanField(label="", required=False)

    class Meta:
        fields = (
            'global_default', 'estimate_label',
            'diagnostic_delay', 'detection_threshold',
            'diagnostic_delay_sigma', 'comment'
        )
        model = IDTTestPropertyEstimate
        widgets = {
            'global_default': forms.HiddenInput()
        }

    def __init__(self, category, *args, **kwargs):
        super(TestPropertyEstimateCreateTestForm, self).__init__(*args, **kwargs)
        self.category = category
        if self.instance.pk and not self.instance.user:
            self.fields['estimate_label'].widget.attrs['readonly'] = True
            self.fields['diagnostic_delay'].widget.attrs['readonly'] = True
            self.fields['detection_threshold'].widget.attrs['readonly'] = True
            self.fields['foursigma_diagnostic_delay_days'].widget.attrs['readonly'] = True
            self.fields['diagnostic_delay_median'].widget.attrs['readonly'] = True
            self.fields['comment'].widget.attrs['readonly'] = True

        self.fields['estimate_label'].widget.attrs['placeholder'] = ''
        self.fields['diagnostic_delay'].widget.attrs['placeholder'] = ''
        self.fields['detection_threshold'].widget.attrs['placeholder'] = ''
        self.fields['diagnostic_delay_sigma'].widget.attrs['placeholder'] = ''
        self.fields['comment'].widget.attrs['placeholder'] = ''

    def clean_diagnostic_delay(self):
        diagnostic_delay = self.cleaned_data['diagnostic_delay']
        if self.category != 'viral_load' and not diagnostic_delay:
            raise forms.ValidationError('This field is required.')
        return diagnostic_delay

    def clean_detection_threshold(self):
        detection_threshold = self.cleaned_data['detection_threshold']
        if self.category == 'viral_load' and not detection_threshold:
            raise forms.ValidationError('Viral Load tests must have a detection threshold.')
        return detection_threshold


class GlobalTestForm(BaseModelForm):

    class Meta:
        model = IDTDiagnosticTest
        fields = ['name', 'category']

    def __init__(self, *args, **kwargs):
        super(GlobalTestForm, self).__init__(*args, **kwargs)
        if self.instance.pk and not self.instance.user:
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['category'].widget.attrs['readonly'] = True
            self.fields['category'].widget.attrs['disabled'] = True


class UserTestForm(BaseModelForm):

    class Meta:
        model = IDTDiagnosticTest
        fields = ['name', 'category']


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

class BaseTestPropertyEstimateFormSet(BaseModelFormSet):

    def __init__(self, test_pk, user, *args, **kwargs):
        self.test_pk = test_pk
        self.user = user
        super(BaseTestPropertyEstimateFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        return super(BaseTestPropertyEstimateFormSet, self)._construct_form(
            i, test_pk=self.test_pk, user=self.user, **kwargs)

TestPropertyEstimateFormSet = modelformset_factory(
    IDTTestPropertyEstimate,
    form=TestPropertyEstimateForm,
    formset=BaseTestPropertyEstimateFormSet
)

class BaseTestPropertyEstimateCreateTestFormSet(BaseModelFormSet):

    def __init__(self, category, *args, **kwargs):
        self.category = category
        super(BaseTestPropertyEstimateCreateTestFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        return super(BaseTestPropertyEstimateCreateTestFormSet, self)._construct_form(
            i, category=self.category, **kwargs)

TestPropertyEstimateCreateTestFormSet = modelformset_factory(
    IDTTestPropertyEstimate,
    form=TestPropertyEstimateCreateTestForm,
    formset=BaseTestPropertyEstimateCreateTestFormSet
)

UserTestPropertyEstimateFormSet = modelformset_factory(
    IDTTestPropertyEstimate,
    form=TestPropertyEstimateForm
)

GlobalTestFormSet = modelformset_factory(
    IDTDiagnosticTest,
    form=GlobalTestForm,
    extra=0
)

UserTestFormSet = modelformset_factory(
    IDTDiagnosticTest,
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


CATEGORIES = (
    ('western_blot', 'Western blot'),
    ('1st_gen_lab', '1st Gen Lab Assay (Viral Lysate IgG sensitive Antibody)'),
    ('2nd_gen_lab', '2nd Gen Lab Assay (Recombinant IgG sensitive Antibody)'),
    ('2nd_gen_rapid', '2nd Gen Rapid Test'),
    ('3rd_gen_lab', '3rd Gen Lab Assay (IgM sensitive Antibody)'),
    ('3rd_gen_rapid', '3rd Gen Rapid Test'),
    ('p24_antigen', 'p24 Antigen'),
    ('4th_gen_lab', '4th Gen Lab Assay (p24 Ag/Ab Combo)'),
    ('4th_gen_rapid', '4th Gen Rapid Test'),
    ('viral_load', 'Viral Load'),
    ('dpp', 'DPP'),
    ('immunofluorescence_assay', 'Immunofluorescence Assay'),
    ('No category', 'No category'),
)

class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset.all()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()

        yield (
            self.field.group_label('Your Tests'),
            [self.choice(ch) for ch in self.queryset.filter(user__isnull=False).order_by('name')]
        )

        for category in CATEGORIES:
            if category[0] != 'No category':
                for group, choices in groupby(
                        self.queryset.filter(user__isnull=True, category=category[0]).order_by('name'),
                        key=lambda row: getattr(row, self.field.group_by_field)
                ):
                    if group:
                        group = category[1]
                    else:
                        group = 'No category'
                    if self.field.group_label(group):
                        yield (
                            self.field.group_label(group),
                            [self.choice(ch) for ch in choices]
                        )
            else:
                for group, choices in groupby(
                        self.queryset.filter(user__isnull=True, category__isnull=True).order_by('name'),
                        key=lambda row: getattr(row, self.field.group_by_field)
                ):
                    if group:
                        group = category[1]
                    else:
                        group = 'No category'
                    if self.field.group_label(group):
                        yield (
                            self.field.group_label(group),
                            [self.choice(ch) for ch in choices]
                        )


class GroupedModelChoiceField(Grouped, ModelChoiceField):
    choices = property(Grouped._get_choices, ModelChoiceField._set_choices)


class GroupedModelMultiChoiceField(Grouped, ModelMultipleChoiceField):
    choices = property(Grouped._get_choices, ModelMultipleChoiceField._set_choices)


class GlobalParametersForm(forms.Form):
    growth_rate = forms.FloatField(required=True, label='Viral load growth rate estimate')
    adjustment_factor = forms.FloatField(required=True, label='Intersubject variability adjustment factor')

    def __init__(self, growth_rate, adjustment_factor, *args, **kwargs):
        super(GlobalParametersForm, self).__init__(*args, **kwargs)
        self.fields['growth_rate'].initial = growth_rate.growth_rate
        self.fields['adjustment_factor'].initial = adjustment_factor.adjustment_factor

    def save(self, user):
        gre = GrowthRateEstimate.objects.get(user=user)
        gre.growth_rate = self.cleaned_data['growth_rate']
        gre.save()
        adj_factor = VariabilityAdjustment.objects.get(user=user)
        adj_factor.adjustment_factor = self.cleaned_data['adjustment_factor']
        adj_factor.save()


class SpecifyInfectiousPeriodForm(BaseModelForm):
    class Meta:
        model = ResidualRisk
        fields = ['infectious_period_input']

    def save(self, commit=True):
        infectious_period = super(SpecifyInfectiousPeriodForm, self).save(commit=False)
        infectious_period.infectious_period = infectious_period.infectious_period_input

        if commit:
            infectious_period.save()

        return infectious_period


class CalculateInfectiousPeriodForm(BaseModelForm):
    class Meta:
        model = ResidualRisk
        fields = ['viral_growth_rate', 'origin_viral_load', 'viral_load']

    def save(self, commit=True):
        infectious_period = super(CalculateInfectiousPeriodForm, self).save(commit=False)

        vlz = infectious_period.origin_viral_load
        vli = infectious_period.viral_load
        vgr = infectious_period.viral_growth_rate
        infectious_period.infectious_period = math.log10(vli/vlz) / vgr

        if commit:
            infectious_period.save()

        return infectious_period

class EstimateWindowResidualRiskForm(forms.Form):
    test = forms.ModelChoiceField(queryset=IDTDiagnosticTest.objects.all(), label=("select test)"), required=True)

    def __init__(self, user, *args, **kwargs):
        super(EstimateWindowResidualRiskForm, self).__init__(*args, **kwargs)
        choices = GroupedModelChoiceField(queryset=IDTDiagnosticTest.objects.filter(Q(user=user) | Q(user=None)), group_by_field='category')
        self.fields['test'] = choices

class CalculateResidualRiskForm(forms.Form):
    incidence = forms.FloatField(required=True, label='Incidence in donor population')
    donations = forms.FloatField(required=True, label='Number of donations per year')

    def calculate_residual_risk(self, window):
        return (window/365)*(self.cleaned_data['incidence']/100)

    def calculate_infectious_donations(self, residual_risk):
        return residual_risk * self.cleaned_data['donations']
