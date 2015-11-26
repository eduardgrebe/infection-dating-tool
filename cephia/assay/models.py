# encoding: utf-8
from django.db import models
from cephia.models import Visit, Specimen, SpecimenType
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


class Panel(models.Model):

    class Meta:
        db_table = "cephia_panels"

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    specimen_type = models.ForeignKey(SpecimenType, null=True, blank=False, db_index=True)
    volume = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class PanelMemberships(models.Model):

    class Meta:
        db_table = "cephia_panel_memberships"

    visit = models.ForeignKey(Visit, null=True, blank=False, db_index=True)
    panel = models.ForeignKey(Panel, null=True, blank=False, db_index=True)
    replicates = models.IntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return self.visit

class PanelShipment(models.Model):

    class Meta:
        db_table = "cephia_panel_shipments"

    specimen = models.ForeignKey(Specimen, null=True, blank=False, db_index=True)
    panel = models.ForeignKey(Panel, null=True, blank=False, db_index=True)
    replicates = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.specimen
