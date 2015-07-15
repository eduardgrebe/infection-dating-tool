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
from file_handlers import get_file_handler_for_type
import logging

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

    patient_label = models.CharField(max_length=255, null=False, blank=True)
    entry_date = models.CharField(max_length=255, null=False, blank=True)
    entry_status = models.CharField(max_length=255, null=False, blank=True)
    country = models.CharField(max_length=255, null=False, blank=True)
    last_negative_date = models.CharField(max_length=255, null=False, blank=True)
    last_positive_date = models.CharField(max_length=255, null=False, blank=True)
    ars_onset = models.CharField(max_length=255, null=False, blank=True)
    fiebig = models.CharField(max_length=255, null=False, blank=True)
    dob = models.CharField(max_length=255, null=False, blank=True)
    gender = models.CharField(max_length=255, null=False, blank=True)
    ethnicity = models.CharField(max_length=255, null=False, blank=True)
    sex_with_men = models.CharField(max_length=255, null=False, blank=True)
    sex_with_women = models.CharField(max_length=255, null=False, blank=True)
    iv_drug_user = models.CharField(max_length=255, null=False, blank=True)
    subtype_confirmed = models.CharField(max_length=255, null=False, blank=True)
    subtype = models.CharField(max_length=255, null=False, blank=True)
    anti_retroviral_initiation_date = models.CharField(max_length=255, null=False, blank=True)
    aids_diagnosis_date = models.CharField(max_length=255, null=False, blank=True)
    treatment_interruption_date = models.CharField(max_length=255, null=False, blank=True)
    treatment_resumption_date = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.patient_label


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
    
    patient_label = models.CharField(max_length=255, null=True, blank=True)
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

    patient_label = models.CharField(max_length=255, null=False, blank=True)
    visit_date = models.CharField(max_length=255, null=False, blank=True)
    status = models.CharField(max_length=255, null=False, blank=True)
    source = models.CharField(max_length=255, null=False, blank=True)
    visit_cd4 = models.CharField(max_length=255, null=False, blank=True)
    visit_vl = models.CharField(max_length=255, null=False, blank=True)
    scope_visit_ec = models.CharField(max_length=255, null=False, blank=True)
    visit_pregnant = models.CharField(max_length=255, null=False, blank=True)
    visit_hepatitis = models.CharField(max_length=255, null=False, blank=True)


    def __unicode__(self):
        return self.visit_label


class Visit(models.Model):

    class Meta:
        db_table = "cephia_visit"


    STATUS_CHOICES = (
        ('negative','Negative'),
        ('positive','Positive'),
        ('unknown','Unkown'),
    )
    

    patient_label = models.CharField(max_length=255, null=False, blank=False)
    visit_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=8, null=False, blank=False, choices=STATUS_CHOICES)
    study = models.ForeignKey(Study, null=True, blank=True)
    visit_cd4 = models.IntegerField(null=True, blank=False)
    visit_vl = models.CharField(max_length=10, null=True, blank=False)
    scope_visit_ec = models.CharField(max_length=100, null=False, blank=True)
    visit_pregnant = models.NullBooleanField()
    visit_hepatitis = models.NullBooleanField()
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
    source_study = models.ForeignKey(Site, null=True, blank=True)
    to_location = models.ForeignKey(Location, null=True, blank=True)
    aliquoting_reason = models.ForeignKey(AliquotingReason, null=True, blank=True)
    panel_inclusion_criteria = models.ForeignKey(PanelInclusionCriteria, null=True, blank=True)


    def __unicode__(self):
        return self.label


class TransferInRow(ImportedRow):

    class Meta:
        db_table = "cephia_transfer_in_row"
        
    specimen_label = models.CharField(max_length=255, null=True, blank=True) 
    patient_label = models.CharField(max_length=255, null=True, blank=True)
    draw_date = models.CharField(max_length=255, null=True, blank=True)
    num_containers = models.CharField(max_length=255, null=True, blank=True)
    transfer_in_date = models.CharField(max_length=255, null=True, blank=True)
    sites = models.CharField(max_length=255, null=True, blank=True)
    transfer_reason = models.CharField(max_length=255, null=True, blank=True)
    spec_type = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.specimen_label

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


class MissingTransferOutRow(ImportedRow):

    class Meta:
        db_table = "cephia_missing_transfer_out_row"
    
    first_aliquot = models.CharField(max_length=255, null=True, blank=True)
    last_aliquot = models.CharField(max_length=255, null=True, blank=True)    
    volume = models.CharField(max_length=255, null=True, blank=True)
    aliquots_created = models.CharField(max_length=255, null=True, blank=True)
    panels_used = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.parent_id


