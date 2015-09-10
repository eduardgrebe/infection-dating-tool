# encoding: utf-8
from lib.fields import ProtectedForeignKey
from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.conf import settings
import os
from file_handlers.file_handler_register import *
import logging
from django.forms.models import model_to_dict
from simple_history.models import HistoricalRecords
import collections

logger = logging.getLogger(__name__)

class CephiaUser(AbstractUser):
    class Meta:
        db_table = "cephia_user"

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Region(models.Model):

    class Meta:
        db_table = "cephia_region"

    name = models.CharField(max_length=100, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Country(models.Model):

    class Meta:
        db_table = "cephia_country"

    code = models.CharField(max_length=5, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    region = ProtectedForeignKey(Region, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.code


class Site(models.Model):
    class Meta:
        db_table = "cephia_site"

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    
    def __unicode__(self):
        return self.name


class Study(models.Model):
    class Meta:
        db_table = "cephia_study"

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return self.name


class Ethnicity(models.Model):

    class Meta:
        db_table = "cephia_ethnicity"

    name = models.CharField(max_length=30, null=False, blank=False)

class Subtype(models.Model):

    class Meta:
        db_table = "cephia_subtype"

    name = models.CharField(max_length=30, null=False, blank=False)


class FileInfo(models.Model):

    class Meta:
        db_table = "cephia_fileinfo"

    STATE_CHOICES = (
        ('pending','Pending'),
        ('imported','Imported'),
        ('validated','Validated'),
        ('error','Error')
    )

    FILE_TYPE_CHOICES = (
        ('subject','Subject'),
        ('visit','Visit'),
        ('transfer_in','Transfer In'),
        ('aliquot','Aliquot'),
        ('transfer_out','Transfer Out'),
    )

    data_file = models.FileField(upload_to=settings.MEDIA_ROOT, null=False, blank=False)
    file_type = models.CharField(max_length=20, null=False, blank=False, choices=FILE_TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=10, null=False, blank=False, default='pending')
    priority = models.IntegerField(null=False, blank=False, default=1)
    message = models.TextField(blank=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.data_file.name

    def filename(self):
        return os.path.basename(self.data_file.name)

    def get_handler(self):
        return get_file_handler_for_type(self.file_type)(self)

    def get_row(self, row_id):
        if self.file_type == 'subject':
            return SubjectRow.objects.get(fileinfo__id=self.id, id=row_id)
        if self.file_type == 'visit':
            return VisitRow.objects.get(fileinfo__id=self.id, id=row_id)
        if self.file_type == 'transfer_in':
            return TransferInRow.objects.get(fileinfo__id=self.id, id=row_id)
        if self.file_type == 'aliquot':
            return AliquotRow.objects.get(fileinfo__id=self.id, id=row_id)
        if self.file_type == 'transfer_out':
            return TransferOutRow.objects.get(fileinfo__id=self.id, id=row_id)

    def get_extension(self):
        return self.filename().split('.')[-1]


class ImportedRow(models.Model):
    class Meta:
        abstract = True
    
    STATE_CHOICES = (
        ('pending','Pending'),
        ('validated','Validated'),
        ('imported','Imported'),
        ('processed','Processed'),
        ('error','Error')
    )

    state = models.CharField(max_length=10, choices=STATE_CHOICES, null=False, blank=False)
    error_message = models.TextField(blank=True)
    date_processed = models.DateTimeField(auto_now_add=True)
    fileinfo = models.ForeignKey(FileInfo)
    history = HistoricalRecords()

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


class ImportedRowComment(models.Model):

    class Meta:
        db_table = "cephia_importedrow_comment"

    comment = models.TextField(blank=False, null=False)
    resolve_date = models.DateTimeField(blank=False, null=False)
    resolve_action = models.TextField(blank=False, null=False)
    assigned_to = models.CharField(max_length=50, null=False, blank=False)

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


class Subject(models.Model):

    class Meta:
        db_table = "cephia_subject"

    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female'),
        ('unkown','Unkown')
    )

    STATUS_CHOICES = (
        ('negative','Negative'),
        ('positive','Positive'),
    )
    
    subject_label = models.CharField(max_length=255, null=True, blank=True)
    cohort_entry_date = models.DateField(null=True, blank=True)
    cohort_entry_hiv_status = models.CharField(max_length=8, null=False, blank=False, choices=STATUS_CHOICES)
    country = models.ForeignKey(Country, null=True, blank=True)
    last_negative_date = models.DateField(null=True, blank=True)
    first_positive_date = models.DateField(null=True, blank=True)
    ars_onset_date = models.DateField(null=True, blank=True)
    fiebig_stage_at_firstpos = models.CharField(max_length=10, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=6, null=False, blank=True, choices=GENDER_CHOICES)
    transgender = models.NullBooleanField()
    population_group = models.ForeignKey(Ethnicity, null=True, blank=True)
    risk_sex_with_men = models.NullBooleanField()
    risk_sex_with_women = models.NullBooleanField()
    risk_idu = models.NullBooleanField()
    subtype_confirmed = models.NullBooleanField()
    subtype = models.ForeignKey(Subtype, null=True, blank=True)
    art_initiation_date = models.DateField(null=True, blank=True)
    aids_diagnosis_date = models.DateField(null=True, blank=True)
    art_interruption_date = models.DateField(null=True, blank=True)
    art_resumption_date = models.DateField(null=True, blank=True)
    artificial = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.subject_label


class SubjectRow(ImportedRow):

    class Meta:
        db_table = "cephia_subjectrow"

    subject_label = models.CharField(max_length=255, null=False, blank=True)
    source_study = models.CharField(max_length=255, null=False, blank=True)
    cohort_entry_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    cohort_entry_date_mm = models.CharField(max_length=255, null=False, blank=True)
    cohort_entry_date_dd = models.CharField(max_length=255, null=False, blank=True)
    cohort_entry_hiv_status = models.CharField(max_length=255, null=False, blank=True)
    country = models.CharField(max_length=255, null=False, blank=True)
    last_negative_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    last_negative_date_mm = models.CharField(max_length=255, null=False, blank=True)
    last_negative_date_dd = models.CharField(max_length=255, null=False, blank=True)
    first_positive_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    first_positive_date_mm = models.CharField(max_length=255, null=False, blank=True)
    first_positive_date_dd = models.CharField(max_length=255, null=False, blank=True)
    fiebig_stage_at_firstpos = models.CharField(max_length=255, null=False, blank=True)
    ars_onset_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    ars_onset_date_mm = models.CharField(max_length=255, null=False, blank=True)
    ars_onset_date_dd = models.CharField(max_length=255, null=False, blank=True)
    date_of_birth_yyyy = models.CharField(max_length=255, null=False, blank=True)
    date_of_birth_mm = models.CharField(max_length=255, null=False, blank=True)
    date_of_birth_dd = models.CharField(max_length=255, null=False, blank=True)
    sex = models.CharField(max_length=255, null=False, blank=True)
    transgender = models.CharField(max_length=255, null=False, blank=True)
    population_group = models.CharField(max_length=255, null=False, blank=True)
    risk_sex_with_men = models.CharField(max_length=255, null=False, blank=True)
    risk_sex_with_women = models.CharField(max_length=255, null=False, blank=True)
    risk_idu = models.CharField(max_length=255, null=False, blank=True)
    subtype = models.CharField(max_length=255, null=False, blank=True)
    subtype_confirmed = models.CharField(max_length=255, null=False, blank=True)
    aids_diagnosis_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    aids_diagnosis_date_mm = models.CharField(max_length=255, null=False, blank=True)
    aids_diagnosis_date_dd = models.CharField(max_length=255, null=False, blank=True)
    art_initiation_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    art_initiation_date_mm = models.CharField(max_length=255, null=False, blank=True)
    art_initiation_date_dd = models.CharField(max_length=255, null=False, blank=True)
    art_interruption_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    art_interruption_date_mm = models.CharField(max_length=255, null=False, blank=True)
    art_interruption_date_dd = models.CharField(max_length=255, null=False, blank=True)
    art_resumption_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    art_resumption_date_mm = models.CharField(max_length=255, null=False, blank=True)
    art_resumption_date_dd = models.CharField(max_length=255, null=False, blank=True)
    comment = models.ForeignKey(ImportedRowComment, blank=False, null=True)
    subject = models.ForeignKey(Subject, null=True, blank=False)

    def __unicode__(self):
        return self.subject_label


class Visit(models.Model):

    class Meta:
        db_table = "cephia_visit"

    STATUS_CHOICES = (
        ('negative','Negative'),
        ('positive','Positive'),
        ('unknown','Unkown'),
    )
    
    subject_label = models.CharField(max_length=255, null=False, blank=False)
    visit_date = models.DateField(null=True, blank=True)
    visit_hivstatus = models.CharField(max_length=8, null=False, blank=False, choices=STATUS_CHOICES)
    source_study = models.ForeignKey(Study, null=True, blank=True)
    cd4_count = models.IntegerField(null=True, blank=False)
    vl = models.CharField(max_length=10, null=True, blank=False)
    scopevisit_ec = models.CharField(max_length=100, null=True, blank=False)
    pregnant = models.NullBooleanField()
    hepatitis = models.NullBooleanField()
    artificial = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, null=True, blank=True, default=None)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.subject_label


class VisitRow(ImportedRow):

    class Meta:
        db_table = "cephia_visitrow"

    subject_label = models.CharField(max_length=255, null=False, blank=True)
    visitdate_yyyy = models.CharField(max_length=255, null=False, blank=True)
    visitdate_mm = models.CharField(max_length=255, null=False, blank=True)
    visitdate_dd = models.CharField(max_length=255, null=False, blank=True)
    visit_hivstatus = models.CharField(max_length=255, null=False, blank=True)
    source_study = models.CharField(max_length=255, null=False, blank=True)
    cd4_count = models.CharField(max_length=255, null=False, blank=True)
    vl = models.CharField(max_length=255, null=False, blank=True)
    scopevisit_ec = models.CharField(max_length=255, null=False, blank=True)
    pregnant = models.CharField(max_length=255, null=False, blank=True)
    hepatitis = models.CharField(max_length=255, null=False, blank=True)
    comment = models.ForeignKey(ImportedRowComment, blank=False, null=True)
    visit = models.ForeignKey(Visit, null=True, blank=False)

    def __unicode__(self):
        return self.subject_label


class SpecimenType(models.Model):

    class Meta:
        db_table = "cephia_specimen_type"

    name = models.CharField(max_length=255, null=False, blank=False)
    spec_type = models.CharField(max_length=10, null=False, blank=False)
    spec_group = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Specimen(models.Model):

    VISIT_LINKAGE_CHOICES = (
        ('provisional','Provisional'),
        ('confirmed','Confirmed'),
        ('artificial','Artificial'),
    )

    class Meta:
        db_table = "cephia_specimen"

    specimen_label = models.CharField(max_length=255, null=True, blank=True)
    parent_label = models.CharField(max_length=255, null=True, blank=True)
    subject_label = models.CharField(max_length=255, null=True, blank=True)
    number_of_containers = models.IntegerField(null=True, blank=True)
    reported_draw_date = models.DateField(null=True, blank=True)
    transfer_in_date = models.DateField(null=True, blank=True)
    transfer_out_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateField(null=True, blank=True)
    transfer_reason = models.CharField(max_length=50, null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=False)
    visit = models.ForeignKey(Visit, null=True, blank=False, related_name='visit')
    visit_linkage = models.CharField(max_length=12, null=True, blank=False, choices=VISIT_LINKAGE_CHOICES)
    specimen_type = models.ForeignKey(SpecimenType, null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    volume_units = models.CharField(max_length=20, null=True, blank=True)
    initial_claimed_volume = models.FloatField(null=True, blank=True)
    source_study = models.ForeignKey(Study, null=True, blank=True)
    receiving_site = models.ForeignKey(Site, null=True, blank=True)
    aliquoting_reason = models.CharField(max_length=20, null=True, blank=True)
    history = HistoricalRecords()


    def __unicode__(self):
        return self.specimen_label


class TransferInRow(ImportedRow):

    class Meta:
        db_table = "cephia_transfer_in_row"

    specimen_label = models.CharField(max_length=255, null=True, blank=True)
    subject_label = models.CharField(max_length=255, null=True, blank=True)
    drawdate_yyyy = models.CharField(max_length=255, null=True, blank=True)
    drawdate_mm = models.CharField(max_length=255, null=True, blank=True)
    drawdate_dd = models.CharField(max_length=255, null=True, blank=True)
    number_of_containers = models.CharField(max_length=255, null=True, blank=True)
    transfer_date_yyyy = models.CharField(max_length=255, null=True, blank=True)
    transfer_date_mm = models.CharField(max_length=255, null=True, blank=True)
    transfer_date_dd = models.CharField(max_length=255, null=True, blank=True)
    receiving_site = models.CharField(max_length=255, null=True, blank=True)
    transfer_reason = models.CharField(max_length=255, null=True, blank=True)
    specimen_type = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    volume_units = models.CharField(max_length=255, null=True, blank=True)
    source_study = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    comment = models.ForeignKey(ImportedRowComment, blank=False, null=True)
    specimen = models.ForeignKey(Specimen, null=True, blank=False)
    roll_up = models.NullBooleanField()


    def __unicode__(self):
        return self.specimen_label


class TransferOutRow(ImportedRow):

    class Meta:
        db_table = "cephia_transfer_out_row"
        
    specimen_label = models.CharField(max_length=255, null=True, blank=True) 
    number_of_containers = models.CharField(max_length=255, null=True, blank=True)
    specimen_type = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    volume_units = models.CharField(max_length=255, null=True, blank=True)
    shipped_in_panel = models.CharField(max_length=255, null=True, blank=True)
    shipment_date_dd = models.CharField(max_length=255, null=True, blank=True)
    shipment_date_mm = models.CharField(max_length=255, null=True, blank=True)
    shipment_date_yyyy = models.CharField(max_length=255, null=True, blank=True)
    destination_site = models.CharField(max_length=255, null=True, blank=True)
    comment = models.ForeignKey(ImportedRowComment, blank=False, null=True)
    specimen = models.ForeignKey(Specimen, null=True, blank=False)

    def __unicode__(self):
        return self.specimen_label


class AliquotRow(ImportedRow):

    class Meta:
        db_table = "cephia_aliquot_row"
        
    parent_label = models.CharField(max_length=255, null=True, blank=True) 
    aliquot_label = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    volume_units = models.CharField(max_length=255, null=True, blank=True)
    number_of_aliquot = models.CharField(max_length=255, null=True, blank=True)
    aliquoting_date_yyyy = models.CharField(max_length=255, null=True, blank=True)
    aliquoting_date_mm = models.CharField(max_length=255, null=True, blank=True)
    aliquoting_date_dd = models.CharField(max_length=255, null=True, blank=True)
    aliquot_reason = models.CharField(max_length=255, null=True, blank=True)
    comment = models.ForeignKey(ImportedRowComment, blank=False, null=True)
    specimen = models.ForeignKey(Specimen, null=True, blank=False)

    def __unicode__(self):
        return self.parent_label
