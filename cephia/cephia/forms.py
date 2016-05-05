from django import forms
from cephia.models import (FileInfo, SubjectRow, Ethnicity,
                           VisitRow, Specimen, TransferInRow,
                           TransferOutRow, AliquotRow, ImportedRowComment, Assay,
                           Laboratory)
from assay.models import (LagSediaResultRow, LagMaximResultRow, ArchitectUnmodifiedResultRow,
                          ArchitectAvidityResultRow, BioRadAvidityCDCResultRow, BioRadAvidityJHUResultRow,
                          BioRadAvidityGlasgowResultRow, VitrosAvidityResultRow, LSVitrosDiluentResultRow,
                          LSVitrosPlasmaResultRow, GeeniusResultRow, BEDResultRow, LuminexCDCResultRow,
                          IDEV3ResultRow)
from diagnostics.models import DiagnosticTestHistoryRow

class BaseFilterForm(forms.Form):

    def get_bool(self, value):
        if value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            return None


class FileInfoForm(forms.ModelForm):

    laboratory = forms.ChoiceField(required=False)

    class Meta:
        model = FileInfo
        fields = ['data_file','file_type', 'priority', 'panel', 'assay']
        widgets = {
            'data_file': forms.FileInput(attrs={'accept':'.xls, .xlsx, .csv'}),
            'priority':forms.HiddenInput(),
            'panel':forms.HiddenInput(),

        }

    def __init__(self, *args, **kwargs):
        super(FileInfoForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

        self.fields['panel'].required = False
        self.fields['assay'].required = False

        lab_choices = [('','---------')]
        [ lab_choices.append((x.id, x.name)) for x in Laboratory.objects.all() ]
        self.fields['laboratory'].choices = lab_choices


class RowCommentForm(forms.ModelForm):
    class Meta:
        ACTION_CHOICES = (
            ('','---------'),
            ('report','Report to developer'),
            ('correct', 'Correct and re-upload'),
        )
        model = ImportedRowComment
        fields = ['resolve_date','resolve_action', 'assigned_to', 'comment']
        widgets = {
            'resolve_date':forms.DateInput(attrs={'class': 'datepicker'}),
            'resolve_action':forms.Select(choices=ACTION_CHOICES)
        }
    
    def __init__(self, *args, **kwargs):
        super(RowCommentForm, self).__init__(*args, **kwargs)
        

class SubjectFilterForm(BaseFilterForm):
    
    GENDER_CHOICES = (
        ('','---------'),
        ('M','Male'),
        ('F','Female'),
    )

    STATUS_CHOICES = (
        ('','---------'),
        ('N','Negative'),
        ('P','Positive'),
    )

    ASSOCIATED_CHOICES = (
        ('','---------'),
        (True,'Yes'),
        (False,'No'),
    )

    subject_label = forms.CharField(max_length=255, required=False)
    cohort_entry_date = forms.DateField(required=False)
    cohort_entry_hiv_status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    sex = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    population_group = forms.ChoiceField(required=False)
    transgender = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    risk_sex_with_men = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    risk_sex_with_women = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    risk_idu = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    subtype_confirmed = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    has_visits = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    
    def __init__(self, *args, **kwargs):
        super(SubjectFilterForm, self).__init__(*args, **kwargs)
        
        self.fields['cohort_entry_date'].widget = forms.DateInput()
        self.fields['cohort_entry_date'].widget.attrs.update({'class':'datepicker'})
        
        ethnicity_choices = [('','---------')]
        [ ethnicity_choices.append((x.id, x.name)) for x in Ethnicity.objects.all() ]
        self.fields['population_group'].choices = ethnicity_choices

    def filter(self, subjects):
        subject_label = self.cleaned_data['subject_label']
        cohort_entry_date = self.cleaned_data['cohort_entry_date']
        cohort_entry_hiv_status = self.cleaned_data['cohort_entry_hiv_status']
        sex = self.cleaned_data['sex']
        population_group = self.cleaned_data['population_group']
        transgender = self.cleaned_data['transgender']
        risk_sex_with_men = self.cleaned_data['risk_sex_with_men']
        risk_sex_with_women = self.cleaned_data['risk_sex_with_women']
        risk_idu = self.cleaned_data['risk_idu']
        subtype_confirmed = self.cleaned_data['subtype_confirmed']
        has_visits = self.cleaned_data['has_visits']

        if subject_label:
            subjects = subjects.filter(subject_label=subject_label)
        if cohort_entry_date:
            subjects = subjects.filter(cohort_entry_date=cohort_entry_date)
        if cohort_entry_hiv_status:
            subjects = subjects.filter(cohort_entry_hiv_status=cohort_entry_hiv_status)
        if sex:
            subjects = subjects.filter(sex=sex)
        if population_group:
            subjects = subjects.filter(population_group__id=population_group)
        if transgender:
            subjects = subjects.filter(transgender=self.get_bool(transgender))
        if risk_sex_with_men:
            subjects = subjects.filter(risk_sex_with_men=self.get_bool(risk_sex_with_men))
        if risk_sex_with_women:
            subjects = subjects.filter(risk_sex_with_women=self.get_bool(risk_sex_with_women))
        if risk_idu:
            subjects = subjects.filter(risk_idu=self.get_bool(risk_idu))
        if subtype_confirmed:
            subjects = subjects.filter(subtype_confirmed=self.get_bool(subtype_confirmed))
        if has_visits:
            subjects = subjects.exclude(visit__isnull=self.get_bool(has_visits))

        return subjects


class VisitFilterForm(forms.Form):

    ASSOCIATED_CHOICES = (
        ('','---------'),
        (True,'Yes'),
        (False,'No'),
    )

    STATUS_CHOICES = (
        ('','---------'),
        ('N','Negative'),
        ('P','Positive'),
    )
    
    subject_label = forms.CharField(max_length=50, required=False)
    visit_date = forms.DateField(required=False)
    visit_hivstatus = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    pregnant = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    hepatitis = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    artificial = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)
    has_subjects = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super(VisitFilterForm, self).__init__(*args, **kwargs)
        self.fields['visit_date'].widget = forms.DateInput()
        self.fields['visit_date'].widget.attrs.update({'class':'datepicker'})

    def filter(self, visits):
        subject_label = self.cleaned_data['subject_label']
        visit_date = self.cleaned_data['visit_date']
        visit_hivstatus = self.cleaned_data['visit_hivstatus']
        pregnant = self.cleaned_data['pregnant']
        hepatitis = self.cleaned_data['hepatitis']
        artificial = self.cleaned_data['artificial']

        if subject_label:
            visits = visits.filter(subject_label=subject_label)
        if visit_date:
            visits = visits.filter(visit_date=visit_date)
        if visit_hivstatus:
            visits = visits.filter(visit_hivstatus=visit_hivstatus)
        if pregnant:
            visits = visits.filter(pregnant=pregnant)
        if hepatitis:
            visits = visits.filter(hepatitis=hepatitis)
        if artificial:
            visits = visits.filter(artificial=artificial)

        return visits
        #visits = visits.exclude(subject__isnull=True)


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

    ASSOCIATED_CHOICES = (
        ('','---------'),
        (True,'Yes'),
        (False,'No'),
    )
    
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)
    has_comment = forms.ChoiceField(choices=ASSOCIATED_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super(RowFilterForm, self).__init__(*args, **kwargs)

    def filter(self, fileinfo):
        if self.is_valid():
            state = self.cleaned_data['state']
            has_comment = self.cleaned_data['has_comment']
        else:
            state = None
            has_comment = None

        if fileinfo.file_type == 'subject':
            rows = SubjectRow.objects.filter(fileinfo=fileinfo)
            template = 'cephia/subject_row_info.html'
        elif fileinfo.file_type == 'visit':
            rows = VisitRow.objects.filter(fileinfo=fileinfo)
            template = 'cephia/visit_row_info.html'
        elif fileinfo.file_type == 'transfer_in':
            rows = TransferInRow.objects.filter(fileinfo=fileinfo)
            template = 'cephia/transfer_in_row_info.html'
        elif fileinfo.file_type == 'aliquot':
            rows = AliquotRow.objects.filter(fileinfo=fileinfo)
            template = 'cephia/aliquot_row_info.html'
        elif fileinfo.file_type == 'transfer_out':
            rows = TransferOutRow.objects.filter(fileinfo=fileinfo)
            template = 'cephia/transfer_out_row_info.html'
        elif fileinfo.file_type == 'test_history':
            rows = DiagnosticTestHistoryRow.objects.filter(fileinfo=fileinfo)
            template = 'diagnostics/test_history_row_info.html'
        elif fileinfo.file_type == 'panel_membership':
            rows = PanelMembershipRow.objects.filter(fileinfo=fileinfo)
            template = 'assay/panel_membership_row_info.html'
        elif fileinfo.file_type == 'panel_shipment':
            rows = PanelShipmentRow.objects.filter(fileinfo=fileinfo)
            template = 'assay/panel_shipment_row_info.html'
        elif fileinfo.file_type == 'assay':
            if fileinfo.assay.name == 'LAg-Sedia':
                rows = LagSediaResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/lag_sedia_row_info.html'
            if fileinfo.assay.name == 'LAg-Maxim':
                rows = LagMaximResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/lag_maxim_row_info.html'
            elif fileinfo.assay.name == 'ArchitectAvidity':
                rows = ArchitectAvidityResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/architect_avidity_row_info.html'
            elif fileinfo.assay.name == 'ArchitectUnmodified':
                rows = ArchitectUnmodifiedResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/architect_unmodified_row_info.html'
            elif fileinfo.assay.name == 'BioRadAvidity-CDC':
                rows = BioRadAvidityCDCResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/biorad_cdc_row_info.html'
            elif fileinfo.assay.name == 'BioRadAvidity-Glasgow':
                rows = BioRadAvidityGlasgowResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/biorad_glasgow_row_info.html'
            elif fileinfo.assay.name == 'BioRadAvidity-JHU':
                rows = BioRadAvidityJHUResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/biorad_jhu_row_info.html'
            elif fileinfo.assay.name == 'Vitros':
                rows = VitrosAvidityResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/vitros_row_info.html'
            elif fileinfo.assay.name == 'LSVitros-Diluent':
                rows = LSVitrosDiluentResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/lsvitros_diluent_row_info.html'
            elif fileinfo.assay.name == 'LSVitros-Plasma':
                rows = LSVitrosPlasmaResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/lsvitros_plasma_row_info.html'
            elif fileinfo.assay.name == 'Geenius':
                rows = GeeniusResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/geenius_row_info.html'
            elif fileinfo.assay.name == 'BED':
                rows = BEDResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/bed_row_info.html'
            elif fileinfo.assay.name == 'BioRad-Avidity-Glasgow':
                rows = VitrosResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/biorad_glasgow_row_info.html'
            elif fileinfo.assay.name == 'BioPlex-CDC':
                rows = LuminexCDCResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/luminex_row_info.html'
            elif fileinfo.assay.name == 'IDE-V3':
                rows = IDEResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/ide_row_info.html'
            elif fileinfo.assay.name == 'Duke-BioPlex':
                rows = DukeResultRow.objects.filter(fileinfo=fileinfo)
                template = 'assay/duke_row_info.html'
        else:
            raise Exception("Unknown filetype : %s" % fileinfo.file_type)

        if state:
            rows = rows.filter(state=state)
        if has_comment:
            if has_comment == 'True':
                rows = rows.filter(comment__isnull=False)
            else:
                rows = rows.filter(comment__isnull=True)

        return rows, template


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
        ('diagnostic_test','Diagnostic Test'),
        ('protocol_lookup','Protocol Lookup'),
        ('test_history','Diagnostic Test History'),
        ('test_property','Diagnostic Test Properties'),
    )

    file_type = forms.ChoiceField(choices=FILE_TYPE_CHOICES, required=False)
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)
    created = forms.DateField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(FileInfoFilterForm, self).__init__(*args, **kwargs)
        self.fields['created'].widget = forms.DateInput()
        self.fields['created'].widget.attrs.update({'class':'datepicker'})

    def filter(self):
        qs = FileInfo.objects.all().order_by('-created')
        file_type = self.cleaned_data['file_type']
        state = self.cleaned_data['state']
        created = self.cleaned_data['created']

        if file_type:
            qs = qs.filter(file_type=file_type)
        if state:
            qs = qs.filter(state=state)
        if created:
            qs = qs.filter(created=created)
            
        return qs

class AssociationFilterForm(forms.Form):

    specimen_label = forms.CharField(required=False)
    subject_label = forms.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(FileInfoFilterForm, self).__init__(*args, **kwargs)

    def filter(self):
        qs = FileInfo.objects.all().order_by('-created')
        specimen_label = self.cleaned_data['specimen_label']
        subject_label = self.cleaned_data['subject_label']

        if specimen_label:
            pass
            #qs = qs.filter(file_type=file_type)
        if subject_label:
            pass
            #qs = qs.filter(state=state)
            
        return qs
