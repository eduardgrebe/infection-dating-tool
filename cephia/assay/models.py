# encoding: utf-8
from django.db import models
from cephia.models import (Visit, Specimen, SpecimenType, ImportedRow,
                           Assay, Laboratory, Panel)
import logging

logger = logging.getLogger(__name__)


class PanelMembershipRow(ImportedRow):

    class Meta:
        db_table = "cephia_panel_membership_rows"

    visit = models.CharField(max_length=255, null=False, blank=True)
    panel = models.CharField(max_length=255, null=False, blank=True)
    replicates = models.CharField(max_length=255, null=False, blank=True)
    category = models.CharField(max_length=255, null=False, blank=True)
    panel_inclusion_criterion = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.visit


class PanelMembership(models.Model):

    class Meta:
        db_table = "cephia_panel_memberships"

    CATEGORY_CHOICES = (
        ('mdri','MDRI'),
        ('frr','FRR'),
        ('challenge','Challenge')
    )

    PANEL_INCLUSION_CHOICES = (
        ('recent_infection_art_naive','Recent Infection ART Naive'),
        ('longstanding_infection_art_naive','Longstanding Infection ART Naive'),
        ('recent_infection_art_surpressed','Recent Infection ART Surpressed'),
        ('longstanding_infection_art_surpressed','Longstanding Infection ART Surpressed'),
        ('recent_infection_art_unsurpressed','Recent Infection ART Unsurpressed'),
        ('longstanding_infection_art_unsurpressed','Longstanding Infection ART Unsurpressed'),
        ('recent_infection_ec','Recent Infection Elite Controller'),
        ('longstanding_infection_ec','Longstanding Infection Elite Controller')
    )

    visit = models.ForeignKey(Visit, null=True, blank=False, db_index=True)
    panel = models.ForeignKey(Panel, null=True, blank=False, db_index=True)
    replicates = models.IntegerField(null=True, blank=False)
    category = models.CharField(max_length=255, null=False, blank=True, choices=CATEGORY_CHOICES)
    panel_inclusion_criterion = models.CharField(max_length=255, null=False, blank=True, choices=PANEL_INCLUSION_CHOICES)

    def __unicode__(self):
        return str(self.visit.id)


class PanelShipmentRow(ImportedRow):

    class Meta:
        db_table = "cephia_panel_shipment_rows"

    specimen = models.CharField(max_length=255, null=False, blank=True)
    panel = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen


class PanelShipment(models.Model):

    class Meta:
        db_table = "cephia_panel_shipments"

    specimen = models.ForeignKey(Specimen, null=True, blank=False, db_index=True)
    panel = models.ForeignKey(Panel, null=True, blank=False, db_index=True)

    def __unicode__(self):
        return self.specimen

class AssayResult(models.Model):

    class Meta:
        db_table = "cephia_assay_results"

    panel = models.ForeignKey(Panel, null=True, blank=False, db_index=True)
    assay = models.ForeignKey(Assay, null=True, blank=False, db_index=True)
    specimen = models.ForeignKey(Specimen, null=True, blank=False, db_index=True)
    reported_date = models.DateField(null=True, blank=False)
    test_date = models.DateField(null=True, blank=False)
    result = models.FloatField(null=True, blank=False)

    def __unicode__(self):
        return self.specimen

class LagResultRow(ImportedRow):

    class Meta:
        db_table = "lag_result_row"

    specimen_label = models.CharField(max_length=255, null=False, blank=True)
    assay = models.CharField(max_length=255, null=False, blank=True)
    laboratory = models.CharField(max_length=255, null=False, blank=True)
    test_date = models.CharField(max_length=255, null=False, blank=True)
    operator = models.CharField(max_length=255, null=False, blank=True)
    assay_kit_lot = models.CharField(max_length=255, null=False, blank=True)
    plate_identifier = models.CharField(max_length=255, null=False, blank=True)
    test_mode = models.CharField(max_length=255, null=False, blank=True)
    well = models.CharField(max_length=255, null=False, blank=True)
    specimen_purpose = models.CharField(max_length=255, null=False, blank=True)
    result_OD = models.CharField(max_length=255, null=False, blank=True)
    result_calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    result_ODn = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen_label

class LagResult(models.Model):

    class Meta:
        db_table = "lag_result"

    specimen = models.ForeignKey(Specimen, null=False, blank=False, db_index=True)
    assay = models.ForeignKey(Assay, null=False, blank=False, db_index=True)
    laboratory = models.ForeignKey(Laboratory, max_length=255, null=True, blank=False)
    test_date = models.DateField(max_length=255, null=False, blank=True)
    operator = models.CharField(max_length=255, null=False, blank=True)
    assay_kit_lot = models.CharField(max_length=255, null=False, blank=True)
    plate_identifier = models.CharField(max_length=255, null=False, blank=True)
    test_mode = models.CharField(max_length=255, null=False, blank=True)
    well = models.CharField(max_length=255, null=False, blank=True)
    specimen_purpose = models.CharField(max_length=255, null=False, blank=True)
    result_OD = models.FloatField(null=True, blank=False)
    result_calibrator_OD = models.FloatField(null=True, blank=False)
    result_ODn = models.FloatField(null=True, blank=False)
    assay_result = models.ForeignKey(AssayResult, null=False, blank=False, db_index=True)

    def __unicode__(self):
        return self.specimen

class BioradResultRow(ImportedRow):

    class Meta:
        db_table = "biorad_result_row"
        
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

# class BioradResult(models.Model):

#     class Meta:
#         db_table = "biorad_result"
        
#     specimen = models.CharField(max_length=255, null=False, blank=True)
#     assay = models.CharField(max_length=255, null=False, blank=True)
#     sample_type = models.CharField(max_length=255, null=False, blank=True)
#     site = models.CharField(max_length=255, null=False, blank=True)
#     test_date = models.CharField(max_length=255, null=False, blank=True)
#     operator = models.CharField(max_length=255, null=False, blank=True)
#     assay_kit_lot_id = models.CharField(max_length=255, null=False, blank=True)
#     plate_id = models.CharField(max_length=255, null=False, blank=True)
#     test_mode = models.CharField(max_length=255, null=False, blank=True)
#     well = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_1 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_2 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_3 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_4 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_5 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_6 = models.CharField(max_length=255, null=False, blank=True)
#     final_result = models.CharField(max_length=255, null=False, blank=True)
#     panel_type = models.CharField(max_length=255, null=False, blank=True)

#     def __unicode__(self):
#         return self.specimen


class ArchitectResultRow(ImportedRow):

    class Meta:
        db_table = "architect_result_row"
        
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

class ArchitectResult(models.Model):

    class Meta:
        db_table = "architect_result"

    specimen = models.ForeignKey(Specimen, null=False, blank=False, db_index=True)
    assay = models.ForeignKey(Assay, null=False, blank=False, db_index=True)
    sample_type = models.CharField(max_length=255, null=False, blank=True)
    laboratory = models.ForeignKey(Laboratory, max_length=255, null=True, blank=False)
    test_date = models.DateField(max_length=255, null=False, blank=True)
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


class VitrosResultRow(ImportedRow):

    class Meta:
        db_table = "vitros_result_row"
        
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

# class VitrosResult(models.Model):

#     class Meta:
#         db_table = "vitros_result"
        
#     specimen = models.CharField(max_length=255, null=False, blank=True)
#     assay = models.CharField(max_length=255, null=False, blank=True)
#     sample_type = models.CharField(max_length=255, null=False, blank=True)
#     site = models.CharField(max_length=255, null=False, blank=True)
#     test_date = models.CharField(max_length=255, null=False, blank=True)
#     operator = models.CharField(max_length=255, null=False, blank=True)
#     assay_kit_lot_id = models.CharField(max_length=255, null=False, blank=True)
#     plate_id = models.CharField(max_length=255, null=False, blank=True)
#     test_mode = models.CharField(max_length=255, null=False, blank=True)
#     well = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_1 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_2 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_3 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_4 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_5 = models.CharField(max_length=255, null=False, blank=True)
#     intermediate_6 = models.CharField(max_length=255, null=False, blank=True)
#     final_result = models.CharField(max_length=255, null=False, blank=True)
#     panel_type = models.CharField(max_length=255, null=False, blank=True)

#     def __unicode__(self):
#         return self.specimen

class LSVitrosResultRow(ImportedRow):

    class Meta:
        db_table = "ls_vitros_result_row"

    specimen_label = models.CharField(max_length=255, null=False, blank=True)
    assay = models.CharField(max_length=255, null=False, blank=True)
    laboratory = models.CharField(max_length=255, null=False, blank=True)
    test_date = models.CharField(max_length=255, null=False, blank=True)
    operator = models.CharField(max_length=255, null=False, blank=True)
    assay_kit_lot = models.CharField(max_length=255, null=False, blank=True)
    plate_identifier = models.CharField(max_length=255, null=False, blank=True)
    well = models.CharField(max_length=255, null=False, blank=True)
    test_mode = models.CharField(max_length=255, null=False, blank=True)
    specimen_purpose = models.CharField(max_length=255, null=False, blank=True)
    result_SCO = models.CharField(max_length=255, null=False, blank=True)
    panel_type = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen

class LSVitrosResult(models.Model):

    class Meta:
        db_table = "ls_vitros_result"

    specimen = models.ForeignKey(Specimen, null=False, blank=False, db_index=True)
    assay = models.ForeignKey(Assay, null=False, blank=False, db_index=True)
    laboratory = models.ForeignKey(Laboratory, max_length=255, null=True, blank=False)
    test_date = models.DateField(max_length=255, null=False, blank=True)
    operator = models.CharField(max_length=255, null=False, blank=True)
    assay_kit_lot = models.CharField(max_length=255, null=False, blank=True)
    plate_identifier = models.CharField(max_length=255, null=False, blank=True)
    well = models.CharField(max_length=255, null=False, blank=True)
    test_mode = models.CharField(max_length=255, null=False, blank=True)
    specimen_purpose = models.CharField(max_length=255, null=False, blank=True)
    result_SCO = models.FloatField(max_length=255, null=False, blank=True)
    panel_type = models.CharField(max_length=255, null=False, blank=True)
    test_date = models.DateField(max_length=255, null=False, blank=True)
    assay_result = models.ForeignKey(AssayResult, null=False, blank=False, db_index=True)

    def __unicode__(self):
        return self.specimen


class BEDResultRow(ImportedRow):

    class Meta:
        db_table = "bed_result_row"

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

class BEDResult(models.Model):

    class Meta:
        db_table = "bed_result"

    specimen = models.ForeignKey(Specimen, null=False, blank=False, db_index=True)
    assay = models.ForeignKey(Assay, null=False, blank=False, db_index=True)
    sample_type = models.CharField(max_length=255, null=False, blank=True)
    laboratory = models.ForeignKey(Laboratory, max_length=255, null=True, blank=False)
    test_date = models.DateField(max_length=255, null=False, blank=True)
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

class GeeniusResultRow(ImportedRow):

    class Meta:
        db_table = "geenius_result_row"
        
    blinded_id = models.CharField(max_length=255, null=False, blank=True)
    assay = models.CharField(max_length=255, null=False, blank=True)
    samples = models.CharField(max_length=255, null=False, blank=True)
    site = models.CharField(max_length=255, null=False, blank=True)
    test_date = models.CharField(max_length=255, null=False, blank=True)
    operator = models.CharField(max_length=255, null=False, blank=True)
    assay_kit_lot_id = models.CharField(max_length=255, null=False, blank=True)
    plate_id = models.CharField(max_length=255, null=False, blank=True)
    test_mode = models.CharField(max_length=255, null=False, blank=True)
    well = models.CharField(max_length=255, null=False, blank=True)
    gp36 = models.CharField(max_length=255, null=False, blank=True)
    gp140 = models.CharField(max_length=255, null=False, blank=True)
    gp160 = models.CharField(max_length=255, null=False, blank=True)
    gp41 = models.CharField(max_length=255, null=False, blank=True)
    p24 = models.CharField(max_length=255, null=False, blank=True)
    p31 = models.CharField(max_length=255, null=False, blank=True)
    ctrl = models.CharField(max_length=255, null=False, blank=True)
    summary = models.CharField(max_length=255, null=False, blank=True)
    biorad_confirmatory_result = models.CharField(max_length=255, null=False, blank=True)
    panel_type = models.CharField(max_length=255, null=False, blank=True)
    exclude = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen
