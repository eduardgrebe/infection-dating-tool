# encoding: utf-8
from django.db import models
from cephia.models import Visit, Specimen, SpecimenType, ImportedRow
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


class PanelMembershipRow(ImportedRow):

    class Meta:
        db_table = "cephia_panel_membership_rows"

    visit = models.CharField(max_length=255, null=False, blank=True)
    panel = models.CharField(max_length=255, null=False, blank=True)
    replicates = models.CharField(max_length=255, null=False, blank=True)
    
    def __unicode__(self):
        return self.visit


class PanelMembership(models.Model):

    class Meta:
        db_table = "cephia_panel_memberships"

    visit = models.ForeignKey(Visit, null=True, blank=False, db_index=True)
    panel = models.ForeignKey(Panel, null=True, blank=False, db_index=True)
    replicates = models.IntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return self.visit


class PanelShipmentRow(ImportedRow):

    class Meta:
        db_table = "cephia_panel_shipment_rows"

    specimen = models.CharField(max_length=255, null=False, blank=True)
    panel = models.CharField(max_length=255, null=False, blank=True)
    replicates = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen


class PanelShipment(models.Model):

    class Meta:
        db_table = "cephia_panel_shipments"

    specimen = models.ForeignKey(Specimen, null=True, blank=False, db_index=True)
    panel = models.ForeignKey(Panel, null=True, blank=False, db_index=True)
    replicates = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.specimen

class LagResultRow(ImportedRow):

    class Meta:
        db_table = "lag_result_row"
        
    specimen = models.CharField(max_length=255, null=False, blank=True)
    assay = models.CharField(max_length=255, null=False, blank=True)
    sample_type = models.CharField(max_length=255, null=False, blank=True)
    site = models.CharField(max_length=255, null=False, blank=True)
    test_date = models.CharField(max_length=255, null=False, blank=True)
    operator = models.CharField(max_length=255, null=False, blank=True)
    assay_kit_lot_id = models.CharField(max_length=255, null=False, blank=True)
    plate_id = models.CharField(max_length=255, null=False, blank=True)
    test_mode = models.CharField(max_length=255, null=False, blank=True)
    well = models.CharField(max_length=255, null=False, blank=True)
    intermediate_1 = models.CharField(max_length=255, null=False, blank=True)
    intermediate_2 = models.CharField(max_length=255, null=False, blank=True)
    intermediate_3 = models.CharField(max_length=255, null=False, blank=True)
    intermediate_4 = models.CharField(max_length=255, null=False, blank=True)
    intermediate_5 = models.CharField(max_length=255, null=False, blank=True)
    intermediate_6 = models.CharField(max_length=255, null=False, blank=True)
    final_result = models.CharField(max_length=255, null=False, blank=True)
    panel_type = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen
