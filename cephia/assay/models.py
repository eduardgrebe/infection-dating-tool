# encoding: utf-8
from django.db import models
import logging

logger = logging.getLogger(__name__)

class Assay(models.Model):
    class Meta:
        db_table = "cephia_assays"

    short_name = models.CharField(max_length=255, null=False, blank=False)
    long_name = models.CharField(max_length=255, null=False, blank=False)
    developer = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return "%s" % (self.name)
