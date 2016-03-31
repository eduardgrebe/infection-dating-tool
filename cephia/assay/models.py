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


    UNIT_CHOICES = (
        ('ODn','Normalised Optical Density'),
        ('OD','Optical Density'),
        ('SCO','Signal/Cutoff Ratio'),
        ('AI','Avidity Index'),
        ('GeeniusIndex','Geenius Index'),
        ('LuminexIndex','Luminex Index'),
        ('IDEV3Conclusion','IDE-V3 Conclusion'),
    )

    panel = models.ForeignKey(Panel, null=True, blank=False, db_index=True)
    assay = models.ForeignKey(Assay, null=True, blank=False, db_index=True)
    specimen = models.ForeignKey(Specimen, null=True, blank=False, db_index=True)
    reported_date = models.DateField(null=True, blank=False)
    test_date = models.DateField(null=True, blank=False)
    result = models.FloatField(null=True, blank=False)
    result_unit = models.CharField(max_length=10, null=True, blank=False, choices=UNIT_CHOICES)

    def __unicode__(self):
        return self.specimen

class BaseAssayResult(models.Model):

    class Meta:
        abstract = True

    specimen = models.ForeignKey(Specimen, null=False, blank=False, db_index=True)
    assay = models.ForeignKey(Assay, null=False, blank=False, db_index=True)
    panel = models.ForeignKey(Panel, null=True, blank=False, db_index=True)
    assay_result = models.ForeignKey(AssayResult, null=True, blank=False, db_index=True)
    laboratory = models.ForeignKey(Laboratory, max_length=255, null=True, blank=False)
    test_date = models.DateField(max_length=255, null=False, blank=True)
    operator = models.CharField(max_length=255, null=False, blank=True)
    assay_kit_lot = models.CharField(max_length=255, null=False, blank=True)
    plate_identifier = models.CharField(max_length=255, null=False, blank=True)
    test_mode = models.CharField(max_length=255, null=False, blank=True)
    well = models.CharField(max_length=255, null=False, blank=True)
    specimen_purpose = models.CharField(max_length=255, null=False, blank=True)


class BaseAssayResultRow(ImportedRow):

    class Meta:
        abstract = True

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


class LagSediaResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "lagsedia_row"

    result_OD = models.CharField(max_length=255, null=False, blank=True)
    result_calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    result_ODn = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen_label


class LagSediaResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_lagsedia"

    result_OD = models.FloatField(null=True, blank=False)
    result_calibrator_OD = models.FloatField(null=True, blank=False)
    result_ODn = models.FloatField(null=True, blank=False)

    def __unicode__(self):
        return self.specimen


class LagMaximResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "lag_maxim_row"

    result_OD = models.CharField(max_length=255, null=False, blank=True)
    result_calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    result_ODn = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen_label


class LagMaximResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_lagmaxim"

    result_OD = models.FloatField(null=True, blank=False)
    result_calibrator_OD = models.FloatField(null=True, blank=False)
    result_ODn = models.FloatField(null=True, blank=False)

    def __unicode__(self):
        return self.specimen.specimen_label


class ArchitectUnmodifiedResultRow(BaseAssayResultRow):
    class Meta:
        db_table = "architect_unmodified_row"

    result_SCO = models.CharField(max_length=255, null=False, blank=True)


class ArchitectUnmodifiedResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_architectunmodified"

    result_SCO = models.FloatField(null=True, blank=False)


class ArchitectAvidityResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "architect_avidity_row"

    result_treated_SCO = models.CharField(max_length=255, null=False, blank=True)
    result_untreated_SCO = models.CharField(max_length=255, null=False, blank=True)
    result_AI = models.CharField(max_length=255, null=False, blank=True)
    result_AI_recalc = models.CharField(max_length=255, null=False, blank=True)
    result_SCO = models.CharField(max_length=255, null=False, blank=True)


class ArchitectAvidityResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_architectavidity"

    result_treated_SCO = models.FloatField(null=True, blank=False)
    result_untreated_SCO = models.FloatField(null=True, blank=False)
    result_AI = models.FloatField(null=True, blank=False)
    result_AI_recalc = models.FloatField(null=True, blank=False)


class BioRadAvidityCDCResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "biorad_avidity_cdc_row"

    result_treated_OD = models.CharField(max_length=255, null=False, blank=True)
    result_untreated_OD = models.CharField(max_length=255, null=False, blank=True)
    result_AI = models.CharField(max_length=255, null=False, blank=True)
    result_AI_recalc = models.CharField(max_length=255, null=False, blank=True)


class BioRadAvidityCDCResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_bioradavidity_cdc"

    result_treated_OD = models.FloatField(null=True, blank=False)
    result_untreated_OD = models.FloatField(null=True, blank=False)
    result_AI = models.FloatField(null=True, blank=False)
    result_AI_recalc = models.FloatField(null=True, blank=False)


class BioRadAvidityJHUResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "biorad_avidity_jhu_row"

    result_treated_OD = models.CharField(max_length=255, null=False, blank=True)
    result_untreated_OD = models.CharField(max_length=255, null=False, blank=True)
    result_AI = models.CharField(max_length=255, null=False, blank=True)
    result_AI_recalc = models.CharField(max_length=255, null=False, blank=True)


class BioRadAvidityJHUResult(BaseAssayResult):
    class Meta:
        db_table = "assayresult_bioradavidity_jhu"

    result_treated_OD = models.FloatField(null=True, blank=False)
    result_untreated_OD = models.FloatField(null=True, blank=False)
    result_AI = models.FloatField(null=True, blank=False)
    result_AI_recalc = models.FloatField(null=True, blank=False)


class BioRadAvidityGlasgowResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "biorad_avidity_glasgow_row"

    result_treated_OD = models.CharField(max_length=255, null=False, blank=True)
    result_untreated_OD = models.CharField(max_length=255, null=False, blank=True)
    result_AI = models.CharField(max_length=255, null=False, blank=True)
    result_AI_recalc = models.CharField(max_length=255, null=False, blank=True)
    result_clasification = models.CharField(max_length=255, null=False, blank=True)
    dilution = models.CharField(max_length=255, null=False, blank=True)


class BioRadAvidityGlasgowResult(BaseAssayResult):
    class Meta:
        db_table = "assayresult_bioradavidity_glasgow"

    result_treated_OD = models.FloatField(null=True, blank=False)
    result_untreated_OD = models.FloatField(null=True, blank=False)
    result_AI = models.FloatField(null=True, blank=False)
    result_AI_recalc = models.FloatField(null=True, blank=False)
    result_clasification = models.CharField(max_length=255, null=False, blank=True)
    dilution = models.CharField(max_length=255, null=False, blank=True)


class VitrosAvidityResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "vitros_avidity_row"

    result_treated_SCO = models.CharField(max_length=255, null=False, blank=True)
    result_untreated_SCO = models.CharField(max_length=255, null=False, blank=True)
    result_AI = models.CharField(max_length=255, null=False, blank=True)
    result_AI_recalc = models.CharField(max_length=255, null=False, blank=True)


class VitrosAvidityResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_vitrosavidity"

    result_treated_SCO = models.FloatField(null=True, blank=False)
    result_untreated_SCO = models.FloatField(null=True, blank=False)
    result_AI = models.FloatField(null=True, blank=False)
    result_AI_recalc = models.FloatField(null=True, blank=False)


class LSVitrosDiluentResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "lsvitros_diluent_row"

    result_SCO = models.CharField(max_length=255, null=False, blank=True)


class LSVitrosDiluentResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_lsvitros_diluent"

    result_SCO = models.FloatField(null=True, blank=False)


class LSVitrosPlasmaResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "lsvitros_plasma_row"

    result_SCO = models.CharField(max_length=255, null=False, blank=True)


class LSVitrosPlasmaResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_lsvitros_plasma"

    result_SCO = models.FloatField(null=True, blank=False)


class GeeniusResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "geenius_row"

    result_gp36_BI = models.CharField(max_length=255, null=False, blank=True)
    result_gp140_BI = models.CharField(max_length=255, null=False, blank=True)
    result_p31_BI = models.CharField(max_length=255, null=False, blank=True)
    result_gp160_BI = models.CharField(max_length=255, null=False, blank=True)
    result_p24_BI = models.CharField(max_length=255, null=False, blank=True)
    result_gp41_BI = models.CharField(max_length=255, null=False, blank=True)
    result_ctrl_BI = models.CharField(max_length=255, null=False, blank=True)
    result_GeeniusIndex = models.CharField(max_length=255, null=False, blank=True)
    result_GeeniusIndex_recalc = models.CharField(max_length=255, null=False, blank=True)


class GeeniusResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_geenius"

    result_gp36_BI = models.FloatField(null=True, blank=False)
    result_gp140_BI = models.FloatField(null=True, blank=False)
    result_p31_BI = models.FloatField(null=True, blank=False)
    result_gp160_BI = models.FloatField(null=True, blank=False)
    result_p24_BI = models.FloatField(null=True, blank=False)
    result_gp41_BI = models.FloatField(null=True, blank=False)
    result_ctrl_BI = models.FloatField(null=True, blank=False)
    result_GeeniusIndex = models.FloatField(null=True, blank=False)
    result_GeeniusIndex_recalc = models.FloatField(null=True, blank=False)


class BEDResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "bed_row"

    result_OD = models.CharField(max_length=255, null=False, blank=True)
    result_calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    result_ODn = models.CharField(max_length=255, null=False, blank=True)
    result_ODn_recalc = models.CharField(max_length=255, null=False, blank=True)


class BEDResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_bed"

    result_OD = models.FloatField(null=True, blank=False)
    result_calibrator_OD = models.FloatField(null=True, blank=False)
    result_ODn = models.FloatField(null=True, blank=False)
    result_ODn_recalc = models.FloatField(null=True, blank=False)


class LuminexCDCResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "luminex_cdc_row"

    result_gp120_n = models.CharField(max_length=255, null=False, blank=True)
    result_gp160_n = models.CharField(max_length=255, null=False, blank=True)
    result_gp41_n = models.CharField(max_length=255, null=False, blank=True)
    result_gp120_a = models.CharField(max_length=255, null=False, blank=True)
    result_gp160_a = models.CharField(max_length=255, null=False, blank=True)
    result_gp41_a = models.CharField(max_length=255, null=False, blank=True)
    result_LuminexIndex = models.CharField(max_length=255, null=False, blank=True)


class LuminexCDCResult(BaseAssayResult):

    class Meta:
        db_table = "assayresult_luminexcdc"

    result_gp120_n = models.FloatField(null=True, blank=False)
    result_gp160_n = models.FloatField(null=True, blank=False)
    result_gp41_n = models.FloatField(null=True, blank=False)
    result_gp120_a = models.FloatField(null=True, blank=False)
    result_gp160_a = models.FloatField(null=True, blank=False)
    result_gp41_a = models.FloatField(null=True, blank=False)
    result_LuminexIndex = models.FloatField(null=True, blank=False)


class IDEV3ResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "ide_v3_row"

    result_tm_OD = models.CharField(max_length=255, null=False, blank=True)
    result_v3_OD = models.CharField(max_length=255, null=False, blank=True)
    result_ratioTM = models.CharField(max_length=255, null=False, blank=True)
    result_ratioV3 = models.CharField(max_length=255, null=False, blank=True)
    result_intermediate = models.CharField(max_length=255, null=False, blank=True)
    result_conclusion = models.CharField(max_length=255, null=False, blank=True)
    result_conclusion_recalc = models.CharField(max_length=255, null=False, blank=True)


class IDEV3Result(BaseAssayResult):

    class Meta:
        db_table = "assayresult_idev3"

    result_tm_OD = models.FloatField(null=True, blank=False)
    result_v3_OD = models.FloatField(null=True, blank=False)
    result_ratioTM = models.FloatField(null=True, blank=False)
    result_ratioV3 = models.FloatField(null=True, blank=False)
    result_intermediate = models.FloatField(null=True, blank=False)
    result_conclusion = models.FloatField(null=True, blank=False)
    result_conclusion_recalc = models.FloatField(null=True, blank=False)
