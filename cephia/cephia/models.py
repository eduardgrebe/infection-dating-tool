# encoding: utf-8
from django.db.models.query import QuerySet
import uuid
from lib.fields import ProtectedForeignKey
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from datetime import datetime, timedelta, date
import pytz
import time
import os
from django.utils import html
from file_handlers.file_handler_register import *
import logging
from django.forms.models import model_to_dict

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
        ('transfer_out','Transfer Out'),
        ('missing_transfer_out','Missing Transfer Out'),
        ('annihilation','Annihilation'),
    )

    data_file = models.FileField(upload_to=settings.MEDIA_ROOT, null=False, blank=False)
    file_type = models.CharField(max_length=20, null=False, blank=False, choices=FILE_TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=10, null=False, blank=False, default='pending')
    priority = models.IntegerField(null=False, blank=False, default=1)
    message = models.TextField(blank=True)
    
    
    def __unicode__(self):
        return self.data_file.name

    def filename(self):
        return os.path.basename(self.data_file.name)

    def get_handler(self):
        return get_file_handler_for_type(self.file_type)(self)


class ImportedRow(models.Model):

    class Meta:
        abstract = True

    STATE_CHOICES = (
        ('pending','Pending'),
        ('processed','Processed'),
        ('error','Error')
    )

    state = models.CharField(max_length=10, choices=STATE_CHOICES, null=False, blank=False)
    error_message = models.TextField(blank=True)
    date_processed = models.DateTimeField(auto_now_add=True)
    fileinfo = models.ForeignKey(FileInfo)


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

    def __unicode__(self):
        return self.patient_label

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
    entry_date = models.DateField(null=True, blank=True)
    entry_status = models.CharField(max_length=8, null=False, blank=False, choices=STATUS_CHOICES)
    country = models.ForeignKey(Country, null=True, blank=True)
    last_negative_date = models.DateField(null=True, blank=True)
    last_positive_date = models.DateField(null=True, blank=True)
    ars_onset = models.DateField(null=True, blank=True)
    fiebig = models.CharField(max_length=10, null=False, blank=False)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, null=False, blank=True, choices=GENDER_CHOICES)
    ethnicity = models.ForeignKey(Ethnicity, null=True, blank=True)
    sex_with_men = models.NullBooleanField()
    sex_with_women = models.NullBooleanField()
    iv_drug_user = models.NullBooleanField()
    subtype_confirmed = models.NullBooleanField()
    subtype = models.ForeignKey(Subtype, null=True, blank=True)
    anti_retroviral_initiation_date = models.DateField(null=True, blank=True)
    aids_diagnosis_date = models.DateField(null=True, blank=True)
    treatment_interruption_date = models.DateField(null=True, blank=True)
    treatment_resumption_date = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.patient_label


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

    def __unicode__(self):
        return self.subject_label

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


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
    status = models.CharField(max_length=8, null=False, blank=False, choices=STATUS_CHOICES)
    study = models.ForeignKey(Study, null=True, blank=True)
    cd4_count = models.IntegerField(null=True, blank=False)
    vl = models.CharField(max_length=10, null=True, blank=False)
    scopevisit_ec = models.CharField(max_length=100, null=False, blank=True)
    pregnant = models.NullBooleanField()
    hepatitis = models.NullBooleanField()
    artificial = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, null=True, blank=True, default=None)

    def __unicode__(self):
        return self.visit_label

    
class SpecimenType(models.Model):

    class Meta:
        db_table = "cephia_specimen_type"
        
    name = models.CharField(max_length=255, null=False, blank=False)
    spec_type = models.CharField(max_length=10, null=False, blank=False)
    spec_group = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name



class Location(models.Model):
    class Meta:
        db_table = "cephia_location"

    name = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return self.name


class Reason(models.Model):
    class Meta:
        db_table = "cephia_reason"

    name = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return self.name

class AliquotingReason(models.Model):

    class Meta:
        db_table = "cephia_aliquoting_reason"
        
    name = models.CharField(max_length=255, null=False, blank=False) 

    def __unicode__(self):
        return self.name

class PanelInclusionCriteria(models.Model):

    class Meta:
        db_table = "cephia_panel_incl_criteria"
        
    name = models.CharField(max_length=255, null=False, blank=False) 

    def __unicode__(self):
        return self.name

    
class Specimen(models.Model):

    class Meta:
        db_table = "cephia_specimen"
    
        
    specimen_label = models.CharField(max_length=255, null=True, blank=True)
    parent_label = models.CharField(max_length=255, null=True, blank=True)
    num_containers = models.IntegerField(null=True, blank=True)
    reported_draw_date = models.DateField(null=True, blank=True)
    transfer_in_date = models.DateField(null=True, blank=True)
    transfer_out_date = models.DateField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True)
    modified_date = models.DateField(null=True, blank=True)
    reason = models.ForeignKey(Reason, null=True, blank=True)
    subject = models.ForeignKey(Subject, null=True, blank=True)
    visit = models.ForeignKey(Visit, null=True, blank=True)
    spec_type = models.ForeignKey(SpecimenType, null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    initial_claimed_volume = models.FloatField(null=True, blank=True)
    other_ref = models.CharField(max_length=10, null=True, blank=True)
    source_study = models.ForeignKey(Study, null=True, blank=True)
    to_location = models.ForeignKey(Location, null=True, blank=True)
    aliquoting_reason = models.ForeignKey(AliquotingReason, null=True, blank=True)
    panel_inclusion_criteria = models.ForeignKey(PanelInclusionCriteria, null=True, blank=True)


    def __unicode__(self):
        return self.label


class TransferInRow(ImportedRow):

    class Meta:
        db_table = "cephia_transfer_in_row"

    specimen_label = models.CharField(max_length=255, null=True, blank=True)
    subject_label = models.CharField(max_length=255, null=True, blank=True)
    drawdate_year = models.CharField(max_length=255, null=True, blank=True)
    drawdate_month = models.CharField(max_length=255, null=True, blank=True)
    drawdate_day = models.CharField(max_length=255, null=True, blank=True)
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
    visit_linkage = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.specimen_label

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


class TransferOutRow(ImportedRow):

    class Meta:
        db_table = "cephia_transfer_out_row"
        
    specimen_label = models.CharField(max_length=255, null=True, blank=True) 
    num_containers = models.CharField(max_length=255, null=True, blank=True)
    transfer_out_date = models.CharField(max_length=255, null=True, blank=True)
    to_location = models.CharField(max_length=255, null=True, blank=True)
    transfer_reason = models.CharField(max_length=255, null=True, blank=True)
    spec_type = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    other_ref = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.specimen_label

class AnnihilationRow(ImportedRow):

    class Meta:
        db_table = "cephia_annihilation_row"
        
    parent_id = models.CharField(max_length=255, null=True, blank=True) 
    child_id = models.CharField(max_length=255, null=True, blank=True)
    child_volume = models.CharField(max_length=255, null=True, blank=True)
    number_of_aliquot = models.CharField(max_length=255, null=True, blank=True)
    annihilation_date = models.CharField(max_length=255, null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    panel_type = models.CharField(max_length=255, null=True, blank=True)
    panel_inclusion_criteria = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.parent_id


