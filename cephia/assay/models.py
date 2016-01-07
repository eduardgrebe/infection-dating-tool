# encoding: utf-8
from django.db import models
from cephia.models import (Visit, Specimen, SpecimenType, ImportedRow, Panels,
                           Assay, Laboratory)
import logging

logger = logging.getLogger(__name__)

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
    panel = models.ForeignKey(Panels, null=True, blank=False, db_index=True)
    replicates = models.IntegerField(null=True, blank=True)
    
    def __unicode__(self):
        return str(self.visit.id)


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
    panel = models.ForeignKey(Panels, null=True, blank=False, db_index=True)
    replicates = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.specimen

class AssayResult(models.Model):

    class Meta:
        db_table = "cephia_assay_results"

    panel = models.ForeignKey(Panels, null=True, blank=False, db_index=True)
    assay = models.ForeignKey(Assay, null=True, blank=False, db_index=True)
    specimen = models.ForeignKey(Specimen, null=True, blank=False, db_index=True)
    test_date = models.DateField(null=True, blank=False)
    result = models.FloatField(null=True, blank=False)

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

class LagResult(models.Model):

    class Meta:
        db_table = "lag_result"
        
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

# class LSVitrosResult(models.Model):

#     class Meta:
#         db_table = "ls_vitros_result"
        
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
