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
