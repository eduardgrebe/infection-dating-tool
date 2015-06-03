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
    state = models.CharField(choices=STATE_CHOICES, max_length=8, null=False, blank=False, default='PE')
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
