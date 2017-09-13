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
from cephia.excel_helper import ExcelHelper
import unicodecsv as csv
import os
from scipy.stats import chi2

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
    screening_test = forms.ModelChoiceField(queryset=IDTDiagnosticTest.objects.all(), label=("select test)"), required=True)

    def __init__(self, *args, **kwargs):
        super(SpecifyInfectiousPeriodForm, self).__init__(*args, **kwargs)
        user = self.instance.user
        choices = GroupedModelChoiceField(queryset=IDTDiagnosticTest.objects.filter(Q(user=user) | Q(user=None)), group_by_field='category')
        self.fields['screening_test'] = choices

    class Meta:
        model = ResidualRisk
        fields = ['infectious_period_input', 'screening_test']

    def save(self, commit=True):
        residual_risk = super(SpecifyInfectiousPeriodForm, self).save(commit=False)
        residual_risk.infectious_period = residual_risk.infectious_period_input
        residual_risk.choice = 'estimates'

        if commit:
            residual_risk.save()

        return residual_risk


class SupplyResidualRiskForm(BaseModelForm):

    class Meta:
        model = ResidualRisk
        fields = ['residual_risk_input']

    def save(self, commit=True):
        residual_risk = super(SupplyResidualRiskForm, self).save(commit=False)
        residual_risk.residual_risk = residual_risk.residual_risk_input
        residual_risk.choice = 'supply'
        residual_risk.upper_limit = residual_risk.residual_risk_input * 2

        if commit:
            residual_risk.save()

        return residual_risk


class DataResidualRiskForm(BaseModelForm):
    interval_list = forms.CharField(required=False, widget=forms.Textarea())
    interval_file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(DataResidualRiskForm, self).__init__(*args, **kwargs)
        user = self.instance.user
        choices = GroupedModelChoiceField(queryset=IDTDiagnosticTest.objects.filter(Q(user=user) | Q(user=None)), group_by_field='category')
        self.fields['positive_test'] = choices
        self.fields['negative_test'] = choices

    class Meta:
        model = ResidualRisk
        fields = ['positive_test', 'negative_test', 'confirmed_transmissions']

    def clean_interval_file(self):
        interval_file = self.cleaned_data.get('interval_file')
        if not interval_file:
            return interval_file
        filename = interval_file.name
        extension = os.path.splitext(filename)[1][1:].lower()
        if extension == 'csv':
            rows = (float(z[0]) for z in csv.reader(interval_file) if z)
        elif extension in ['xls', 'xlsx']:
            rows = (float(z[0]) for z in ExcelHelper(interval_file).rows() if z)
        else:
            raise forms.ValidationError('Unsupported file uploaded: Only CSV and Excel are allowed.')
        self.cleaned_data['imported_intervals'] = [r for r in rows if r]
        return interval_file

    def clean_interval_list(self):
        value = self.cleaned_data.get('interval_list')
        if not value:
            return value
        rows = [float(z.strip()) for z in value.split(u'\n') if z and z != '\r']
        self.cleaned_data['imported_intervals'] = rows
        return value

    def clean(self):
        if self.cleaned_data.get('interval_file') and self.cleaned_data.get('interval_list'):
            raise forms.ValidationError('You must upload either a file or a list of inter donation intervals, not both.')
        if not self.cleaned_data.get('interval_file') and not self.cleaned_data.get('interval_list'):
            raise forms.ValidationError('You must upload either a file or list of inter donation intervals.')

        return self.cleaned_data

    def save(self, user, commit=True):
        residual_risk = super(DataResidualRiskForm, self).save(commit=False)
        intervals = self.cleaned_data['imported_intervals']
        d1 = self.cleaned_data['negative_test'].get_diagnostic_delay_for_residual_risk(user)
        d2 = self.cleaned_data['positive_test'].get_diagnostic_delay_for_residual_risk(user)
        calculated_intervals = [1/(x + d1 - d2) for x in intervals]
        total_exposure = sum(calculated_intervals)
        n_i = self.cleaned_data['confirmed_transmissions']

        ci_upper_bound = chi2.ppf(0.975, df=2*n_i)*2*total_exposure
        residual_risk.ci_lower_bound = chi2.ppf(0.025, df=2*n_i)*2*total_exposure
        residual_risk.ci_upper_bound = ci_upper_bound
        residual_risk.residual_risk = n_i / total_exposure
        residual_risk.choice = 'data'
        residual_risk.upper_limit = ci_upper_bound
        if commit:
            residual_risk.save()

        return residual_risk


class CalculateInfectiousPeriodForm(BaseModelForm):
    screening_test = forms.ModelChoiceField(queryset=IDTDiagnosticTest.objects.all(), label=("select test)"), required=True)

    def __init__(self, *args, **kwargs):
        super(CalculateInfectiousPeriodForm, self).__init__(*args, **kwargs)
        user = self.instance.user
        choices = GroupedModelChoiceField(queryset=IDTDiagnosticTest.objects.filter(Q(user=user) | Q(user=None)), group_by_field='category')
        self.fields['screening_test'] = choices

    class Meta:
        model = ResidualRisk
        fields = ['viral_growth_rate', 'origin_viral_load', 'viral_load', 'screening_test']

    def save(self, commit=True):
        residual_risk = super(CalculateInfectiousPeriodForm, self).save(commit=False)

        vlz = residual_risk.origin_viral_load
        vli = residual_risk.viral_load
        vgr = residual_risk.viral_growth_rate
        residual_risk.infectious_period = math.log10(vli/vlz) / vgr
        residual_risk.choice = 'estimates'

        if commit:
            residual_risk.save()

        return residual_risk


class CalculateResidualRiskForm(forms.Form):
    incidence = forms.FloatField(required=True, label='Incidence in donor population')
    donations = forms.FloatField(required=True, label='Number of donations per year')
    upper_limit = forms.FloatField(required=True)

    def __init__(self, upper_limit, *args, **kwargs):
        super(CalculateResidualRiskForm, self).__init__(*args, **kwargs)
        if upper_limit > 0:
            self.fields['upper_limit'].initial = upper_limit

    def calculate_residual_risk(self, window):
        return (window/365)*(self.cleaned_data['incidence']/100)

    def calculate_infectious_donations(self, residual_risk):
        return residual_risk * self.cleaned_data['donations']
