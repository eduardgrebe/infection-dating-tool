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

    data_file = models.FileField(upload_to=settings.MEDIA_ROOT, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=8, null=False, blank=False, default='pending')
    message = models.TextField(blank=True)

    def __unicode__(self):
        return self.data_file.name

    def filename(self):
        return os.path.basename(self.data_file.name)


class ImportedRow(models.Model):

    class Meta:
        abstract = True

    STATE_CHOICES = (
        ('pending','Pending'),
        ('processed','Processed'),
        ('error','Error')
    )

    state = models.CharField(max_length=9, choices=STATE_CHOICES, null=False, blank=False)
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
        ('pending','Pending'),
        ('processed','Processed'),
        ('error','Error')
    )
    
    patient_label = models.CharField(max_length=255, null=False, blank=False)
    entry_date = models.DateField(max_length=255, null=False, blank=True)
    entry_status = models.CharField(max_length=255, null=False, blank=False)
    country = models.CharField(max_length=255, null=False, blank=False)
    last_negative_date = models.DateField(null=False, blank=True)
    last_positive_date = models.DateField(null=False, blank=True)
    ars_onset = models.DateField(null=False, blank=False)
    fiebig = models.CharField(max_length=10, null=False, blank=False)
    dob = models.DateField(null=False, blank=True)
    gender = models.CharField(max_length=6, null=False, blank=True, choices=GENDER_CHOICES)
    ethnicity = models.CharField(max_length=50, null=False, blank=False)
    sex_with_men = models.NullBooleanField()
    sex_with_women = models.NullBooleanField()
    iv_drug_user = models.NullBooleanField()
    subtype_confirmed = models.NullBooleanField()
    subtype = models.CharField(max_length=255, null=False, blank=False)
    anti_retroviral_initiation_date = models.DateField(null=False, blank=False)
    aids_diagnosis_date = models.DateField(null=False, blank=False)
    treatment_interruption_date = models.DateField(null=False, blank=False)
    treatment_resumption_date = models.DateField(null=False, blank=False)

    def __unicode__(self):
        return self.patient_label
