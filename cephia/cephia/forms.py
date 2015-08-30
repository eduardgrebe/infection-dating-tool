from django import forms
from models import FileInfo, ImportedRowComment, Specimen


class FileInfoForm(forms.ModelForm):
    class Meta:
        model = FileInfo
        fields = ['data_file','file_type', 'priority']
        widgets = {
            'data_file': forms.FileInput(attrs={'accept':'.xls, .xlsx, .csv'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(FileInfoForm, self).__init__(*args, **kwargs)
        
        for key in self.fields:
            self.fields[key].required = True


class RowCommentForm(forms.ModelForm):
    class Meta:
        ACTION_CHOICES = (
            ('action1','Action1'),
            ('action2', 'Action2'),
        )
        model = ImportedRowComment
        fields = ['resolve_date','resolve_action', 'assigned_to', 'comment']
        widgets = {
            'resolve_date':forms.DateInput(attrs={'class': 'datepicker'}),
            'resolve_action':forms.Select(choices=ACTION_CHOICES)
        }
    
    def __init__(self, *args, **kwargs):
        super(RowCommentForm, self).__init__(*args, **kwargs)
        

class SubjectFilterForm(forms.Form):
    
    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female'),
        ('unkown','Unkown')
    )

    STATUS_CHOICES = (
        ('','---------'),
        ('negative','Negative'),
        ('positive','Positive'),
    )

    ASSOCIATED_CHOICES = (
        ('','---------'),
        ('yes','Yes'),
        ('no','No'),
    )
    
    subject_label = forms.CharField(max_length=255)
    cohort_entry_date = forms.DateField()
    cohort_entry_hiv_status = forms.ChoiceField(choices=STATUS_CHOICES)
    last_negative_date = forms.DateField()
    first_positive_date = forms.DateField()
    ars_onset_date = forms.DateField()
    fiebig_stage_at_firstpos = forms.CharField(max_length=10)
    date_of_birth = forms.DateField()
    date_of_death = forms.DateField()
    sex = forms.ChoiceField(choices=GENDER_CHOICES)
    population_group = forms.ChoiceField()
    transgender = forms.BooleanField()
    risk_sex_with_men = forms.BooleanField()
    risk_sex_with_women = forms.BooleanField()
    risk_idu = forms.BooleanField()
    subtype_confirmed = forms.BooleanField()
    art_initiation_date = forms.DateField()
    aids_diagnosis_date = forms.DateField()
    art_interruption_date = forms.DateField()
    art_resumption_date = forms.DateField()
    has_visits = forms.ChoiceField(choices=ASSOCIATED_CHOICES)
    
    def __init__(self, *args, **kwargs):
        super(SubjectFilterForm, self).__init__(*args, **kwargs)

    def filter(self):
        pass


class VisitFilterForm(forms.Form):

    ASSOCIATED_CHOICES = (
        ('','---------'),
        ('yes','Yes'),
        ('no','No'),
    )
    
    subject_label = forms.CharField(max_length=50, required=False)
    visit_date = forms.DateField(required=False)
    visit_hivstatus = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    pregnant = forms.BooleanField(required=False)
    hepatitis = forms.BooleanField(required=False)
    artificial = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(VisitFilterForm, self).__init__(*args, **kwargs)

    def filter(self):
        pass

class SpecimenFilterForm(forms.Form):
    
    specimen_label = forms.CharField(required=False)
    reported_draw_date = forms.DateField(required=False)
    transfer_in_date = forms.DateField(required=False)
    transfer_out_date = forms.DateField(required=False)

    def __init__(self, *args, **kwargs):
        super(SpecimenFilterForm, self).__init__(*args, **kwargs)
        self.fields['reported_draw_date'].widget = forms.DateInput()
        self.fields['reported_draw_date'].widget.attrs.update({'class':'datepicker'})
        self.fields['transfer_in_date'].widget = forms.DateInput()
        self.fields['transfer_in_date'].widget.attrs.update({'class':'datepicker'})
        self.fields['transfer_out_date'].widget = forms.DateInput()
        self.fields['transfer_out_date'].widget.attrs.update({'class':'datepicker'})

    def filter(self):
        qs = Specimen.objects.all().order_by('specimen_label', 'parent_label')
        reported_draw_date = self.cleaned_data['reported_draw_date']
        transfer_in_date = self.cleaned_data['transfer_in_date']
        transfer_out_date = self.cleaned_data['transfer_out_date']
        specimen_label = self.cleaned_data['specimen_label']

        if transfer_out_date:
            qs = qs.filter(transfer_out_date=transfer_out_date)
        if transfer_in_date:
            qs = qs.filter(transfer_in_date=transfer_in_date)
        if reported_draw_date:
            qs = qs.filter(reported_draw_date=reported_draw_date)
        if specimen_label:
            qs = qs.filter(specimen_label=specimen_label)
                
        return qs


class RowFilterForm(forms.Form):

    STATE_CHOICES = (
        ('','---------'),
        ('pending','Pending'),
        ('validated','Validated'),
        ('processed','Processed'),
        ('error','Error'),
    )
    
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super(RowFilterForm, self).__init__(*args, **kwargs)

    def filter(self):
        pass


class FileInfoFilterForm(forms.Form):

    STATE_CHOICES = (
        ('','---------'),
        ('pending','Pending'),
        ('validated','Validated'),
        ('processed','Processed'),
        ('error','Error'),
    )

    FILE_TYPE_CHOICES = (
        ('','---------'),
        ('subject','Subject'),
        ('visit','Visit'),
        ('transfer_in','Transfer In'),
        ('aliquot','Aliquot'),
        ('transfer_out','Transfer Out'),
    )

    file_type = forms.ChoiceField(choices=FILE_TYPE_CHOICES, required=False)
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)
    
    def __init__(self, *args, **kwargs):
        super(FileInfoFilterForm, self).__init__(*args, **kwargs)

    def filter(self):
        qs = FileInfo.objects.all().order_by('-created')
        file_type = self.cleaned_data['file_type']
        state = self.cleaned_data['state']

        if file_type:
            qs = qs.filter(file_type=file_type)
        if state:
            qs = qs.filter(state=state)
            
        return qs
