from django import forms
from models import FileInfo

class FileInfoForm(forms.ModelForm):

    FILE_TYPE_CHOICES = (
        ('subject','Subject'),
        ('visit','Visit'),
        ('transfer_in','Transfer In')
    )

    class Meta:
        model = FileInfo
        fields = ['data_file','file_type']
        widgets = {
            'data_file': forms.FileInput(),
        }

# class VisitForm(forms.ModelForm):
    
#     STATUS_CHOICES = (
#         ('negative','Negative'),
#         ('positive','Positive'),
#         ('unknown','Unkown'),
#     )

#     visit_label = forms.CharField(max_length=255, required=True)
#     visit_date = forms.DateField(required=True)
#     status = forms.ChoiceField(max_length=8, required=True, choices=STATUS_CHOICES)
#     source = forms.ForeignKey(Source)
#     visit_cd4 = forms.IntegerField(null=False, blank=False)
#     visit_vl = forms.CharField(max_length=10, null=False, blank=True)
#     scope_visit_ec = forms.CharField(max_length=100, null=False, blank=True)
#     visit_pregnant = forms.BooleanField(required=False)
#     visit_hepatitis = forms.BooleanField(required=False)
#     subject = forms.ForeignKey(Subject, null=True, blank=True, default=None)


# class SubjectForm(forms.Form):

#     GENDER_CHOICES = (
#         ('male','Male'),
#         ('female','Female'),
#         ('unkown','Unkown')
#     )

#     STATUS_CHOICES = (
#         ('negative','Negative'),
#         ('positive','Positive'),
#     )
    
#     patient_label = forms.CharField(max_length=255, required=True)
#     entry_date = forms.DateField(required=False)
#     entry_status = forms.CharField(max_length=8, required=True, choices=STATUS_CHOICES)
#     country = forms.ForeignKey(Country)
#     last_negative_date = forms.DateField(required=False)
#     last_positive_date = forms.DateField(required=False)
#     ars_onset = forms.DateField(required=False)
#     fiebig = forms.CharField(max_length=10, required=True)
#     dob = forms.DateField(required=False)
#     gender = forms.CharField(max_length=6, required=True, choices=GENDER_CHOICES)
#     ethnicity = forms.ForeignKey(Ethnicity)
#     sex_with_men = forms.BooleanField(required=False)
#     sex_with_women = forms.BooleanField(required=False)
#     iv_drug_user = forms.BooleanField(required=False)
#     subtype_confirmed = forms.BooleanField(required=False)
#     subtype = forms.ForeignKey(Subtype)
#     anti_retroviral_initiation_date = forms.DateField(required=False)
#     aids_diagnosis_date = forms.DateField(required=False)
#     treatment_interruption_date = forms.DateField(required=False)
#     treatment_resumption_date = forms.DateField(required=False)


# class SpecimenForm(forms.Form):

#     SITE_CHOICES = (
#         ('BSRI', 'BSRI'),
#         ('PHE', 'PHE'),
#     )
    
#     label = forms.CharField(max_length=255, null=False, blank=False) 
#     num_containers = forms.IntegerField(null=False, blank=False, default=1)
#     reported_draw_date = forms.DateField()
#     transfer_in_date = forms.DateField()
#     to_location = forms.ForeignKey(Location)
#     reason = forms.ForeignKey(Reason)
#     spec_type = forms.ForeignKey(SpecimenType)
#     volume = forms.IntegerField()
#     initial_claimed_volume = forms.IntegerField()
#     other_ref = forms.IntegerField()
#     source_study = forms.ForeignKey(Study)
#     site = forms.CharField(max_length=5, null=False, blank=False, choices=SITE_CHOICES)
