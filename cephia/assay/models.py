# encoding: utf-8
from django.db import models
from cephia.models import (Visit, Specimen, SpecimenType, ImportedRow,
                           Assay, Laboratory, Panel, FileInfo)
from lib.fields import ProtectedForeignKey
from assay_result_factory import *
from django.forms.models import model_to_dict
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


class AssayRun(models.Model):
    class Meta:
        db_table = "cephia_assay_runs"

    panel = ProtectedForeignKey(Panel, null=False, db_index=True)
    assay = ProtectedForeignKey(Assay, null=False, db_index=True)
    laboratory = ProtectedForeignKey(Laboratory, null=False, db_index=True)
    fileinfo = ProtectedForeignKey(FileInfo, null=False, db_index=True)
    run_date = models.DateField(null=False)
    comment = models.CharField(max_length=255, null=True, blank=False)


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
    assay_run = ProtectedForeignKey(AssayRun, null=True, db_index=True)
    reported_date = models.DateField(null=True, blank=False)
    test_date = models.DateField(null=True, blank=False)
    result = models.FloatField(null=True, blank=False)
    unit = models.CharField(max_length=10, null=True, blank=False, choices=UNIT_CHOICES)
    method = models.CharField(max_length=50, null=True, blank=False)
    warning_msg = models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen.specimen_label

    def get_specific_results(self):
        if self.assay:
            result_model = get_results_for_assay(self.assay.name)
            headers = result_model._meta.get_all_field_names()
            results = [ result.model_to_dict() for result in result_model.objects.filter(assay_result=self) ]
            return headers, results

        return None

    def get_specific_results_for_run(self):
        if self.assay:
            result_model = get_result_model(self.assay.name)
            headers = [ header.replace('_id', '') if header.endswith('_id') else header for header in result_model._meta.get_all_field_names() ]
            results = [ result for result in result_model.objects.filter(assay_run=self.assay_run) ]
            return headers, results

        return None

class BaseAssayResult(models.Model):

    class Meta:
        abstract = True

    specimen = models.ForeignKey(Specimen, null=True, db_index=True)
    assay = models.ForeignKey(Assay, null=True, blank=False, db_index=True)
    assay_result = models.ForeignKey(AssayResult, null=True, blank=False, db_index=True)
    laboratory = models.ForeignKey(Laboratory, null=True, blank=False, db_index=True)
    test_date = models.DateField(max_length=255, null=True, blank=True)
    operator = models.CharField(max_length=255, null=True, blank=True)
    assay_kit_lot = models.CharField(max_length=255, null=True, blank=True)
    plate_identifier = models.CharField(max_length=255, null=True, blank=True)
    test_mode = models.CharField(max_length=255, null=True, blank=True)
    specimen_purpose = models.CharField(max_length=255, null=True, blank=True)
    specimen_label = models.CharField(max_length=255, null=True, blank=True)
    assay_run = ProtectedForeignKey(AssayRun, null=True, db_index=True)
    interpretation = models.CharField(max_length=255, null=True, blank=False)
    exclusion = models.CharField(max_length=255, null=True, blank=False)
    warning_msg = models.CharField(max_length=255, null=True, blank=False)

    def save(self, *args, **kwargs):
        for field in self._meta.get_all_field_names():
            if field != 'luminexcdcresultrow':
                if getattr(self, field) == 'NA' and self._meta.get_field(field).get_internal_type() == 'FloatField':
                    setattr(self, field, None)
                if getattr(self, field) == 'NEG' and self._meta.get_field(field).get_internal_type() == 'FloatField':
                    setattr(self, field, None)
                    setattr(self, 'interpretation', 'neg')

        super(BaseAssayResult, self).save(*args, **kwargs)

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


class BaseAssayResultRow(ImportedRow):

    class Meta:
        abstract = True

    specimen_label = models.CharField(max_length=255, null=True, blank=True)
    assay = models.CharField(max_length=255, null=True, blank=True)
    laboratory = models.CharField(max_length=255, null=True, blank=True)
    test_date = models.CharField(max_length=255, null=True, blank=True)
    operator = models.CharField(max_length=255, null=True, blank=True)
    assay_kit_lot = models.CharField(max_length=255, null=True, blank=True)
    plate_identifier = models.CharField(max_length=255, null=True, blank=True)
    test_mode = models.CharField(max_length=255, null=True, blank=True)
    specimen_purpose = models.CharField(max_length=255, null=True, blank=True)
    interpretation = models.CharField(max_length=255, null=True, blank=False)
    exclusion = models.CharField(max_length=255, null=True, blank=False)


class LagSediaResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "lagsedia_row"

    OD = models.CharField(max_length=255, null=False, blank=True)
    calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    ODn = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)


    def __unicode__(self):
        return self.specimen_label


class LagSediaResult(BaseAssayResult):

    class Meta:
        db_table = "assaylagsedia"

    OD = models.FloatField(null=True, blank=False)
    calibrator_OD = models.FloatField(null=True, blank=False)
    ODn = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=10, null=False, blank=True)

    def __unicode__(self):
        return self.specimen


class LagMaximResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "lag_maxim_row"

    OD = models.CharField(max_length=255, null=False, blank=True)
    calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    ODn = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.specimen_label


class LagMaximResult(BaseAssayResult):

    class Meta:
        db_table = "assaylagmaxim"

    OD = models.FloatField(null=True, blank=False)
    calibrator_OD = models.FloatField(null=True, blank=False)
    ODn = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=10, null=False, blank=True)

    def __unicode__(self):
        return self.specimen.specimen_label


class ArchitectUnmodifiedResultRow(BaseAssayResultRow):
    class Meta:
        db_table = "architect_unmodified_row"

    SCO = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)


class ArchitectUnmodifiedResult(BaseAssayResult):

    class Meta:
        db_table = "assayarchitectunmodified"

    SCO = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=255, null=False, blank=True)


class ArchitectAvidityResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "architect_avidity_row"

    treated_guanidine_SCO = models.CharField(max_length=255, null=False, blank=True)
    untreated_pbs_SCO = models.CharField(max_length=255, null=False, blank=True)
    AI = models.CharField(max_length=255, null=False, blank=True)
    AI_reported = models.CharField(max_length=255, null=False, blank=True)
    well_treated_guanidine = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_pbs = models.CharField(max_length=255, null=False, blank=True)


class ArchitectAvidityResult(BaseAssayResult):

    class Meta:
        db_table = "assayarchitectavidity"

    treated_guanidine_SCO = models.FloatField(null=True)
    untreated_pbs_SCO = models.FloatField(null=True)
    AI = models.FloatField(null=True)
    AI_reported = models.FloatField(null=True)
    well_treated_guanidine = models.CharField(max_length=10, null=False, blank=True)
    well_untreated_pbs = models.CharField(max_length=10, null=False, blank=True)

    def save(self, *args, **kwargs):
        if self.treated_guanidine_SCO < -1 and self.untreated_pbs_SCO < -1:
            self.AI = None
        super(ArchitectAvidityResult, self).save(*args, **kwargs)



class BioRadAvidityCDCResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "biorad_avidity_cdc_row"

    treated_DEA_OD = models.CharField(max_length=255, null=False, blank=True)
    untreated_dilwashsoln_OD = models.CharField(max_length=255, null=False, blank=True)
    AI_reported = models.CharField(max_length=255, null=False, blank=True)
    AI = models.CharField(max_length=255, null=False, blank=True)
    well_treated_DEA = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_dilwashsoln = models.CharField(max_length=255, null=False, blank=True)


class BioRadAvidityCDCResult(BaseAssayResult):

    class Meta:
        db_table = "assaybioradavidity_cdc"

    treated_DEA_OD = models.FloatField(null=True)
    untreated_dilwashsoln_OD = models.FloatField(null=True)
    AI_reported = models.FloatField(null=True)
    AI = models.FloatField(null=True)
    well_treated_DEA = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_dilwashsoln = models.CharField(max_length=255, null=False, blank=True)


class BioRadAvidityJHUResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "biorad_avidity_jhu_row"

    treated_DEA_OD = models.CharField(max_length=255, null=False, blank=True)
    untreated_dilwashsoln_OD = models.CharField(max_length=255, null=False, blank=True)
    AI_reported = models.CharField(max_length=255, null=False, blank=True)
    AI = models.CharField(max_length=255, null=False, blank=True)
    well_treated_DEA = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_dilwashsoln = models.CharField(max_length=255, null=False, blank=True)


class BioRadAvidityJHUResult(BaseAssayResult):
    class Meta:
        db_table = "assaybioradavidity_jhu"

    treated_DEA_OD = models.FloatField(null=True, blank=False)
    untreated_dilwashsoln_OD = models.FloatField(null=True, blank=False)
    AI_reported = models.FloatField(null=True, blank=False)
    AI = models.FloatField(null=True, blank=False)
    well_treated_DEA = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_dilwashsoln = models.CharField(max_length=255, null=False, blank=True)


class BioRadAvidityGlasgowResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "biorad_avidity_glasgow_row"

    treated_urea_OD = models.CharField(max_length=255, null=True, blank=False)
    untreated_buffer_OD = models.CharField(max_length=255, null=True, blank=False)
    AI_reported = models.CharField(max_length=255, null=True, blank=False)
    AI = models.CharField(max_length=255, null=True, blank=False)
    well_treated_urea = models.CharField(max_length=255, null=True, blank=False)
    well_untreated_buffer = models.CharField(max_length=255, null=True, blank=False)
    dilution = models.CharField(max_length=255, null=True, blank=False)


class BioRadAvidityGlasgowResult(BaseAssayResult):
    class Meta:
        db_table = "assaybioradavidity_glasgow"

    treated_urea_OD = models.FloatField(null=True, blank=False)
    untreated_buffer_OD = models.FloatField(null=True, blank=False)
    AI_reported = models.FloatField(null=True, blank=False)
    AI = models.FloatField(null=True, blank=False)
    well_treated_urea = models.CharField(max_length=255, null=True, blank=False)
    well_untreated_buffer = models.CharField(max_length=255, null=True, blank=False)
    dilution = models.CharField(max_length=255, null=True, blank=False)


class VitrosAvidityResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "vitros_avidity_row"

    treated_guanidine_OD = models.CharField(max_length=255, null=False, blank=True)
    untreated_pbs_OD = models.CharField(max_length=255, null=False, blank=True)
    AI = models.CharField(max_length=255, null=False, blank=True)
    AI_reported = models.CharField(max_length=255, null=False, blank=True)
    well_treated_guanidine = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_pbs = models.CharField(max_length=255, null=False, blank=True)


class VitrosAvidityResult(BaseAssayResult):

    class Meta:
        db_table = "assayvitrosavidity"

    treated_guanidine_OD = models.FloatField(max_length=255, null=True)
    untreated_pbs_OD = models.FloatField(max_length=255, null=True)
    AI = models.FloatField(max_length=255, null=True)
    AI_reported = models.FloatField(max_length=255, null=True)
    well_treated_guanidine = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_pbs = models.CharField(max_length=255, null=False, blank=True)


class LSVitrosDiluentResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "lsvitros_diluent_row"

    SCO = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)

class LSVitrosDiluentResult(BaseAssayResult):

    class Meta:
        db_table = "assaylsvitros_diluent"

    SCO = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=10, null=False, blank=True)


class LSVitrosPlasmaResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "lsvitros_plasma_row"

    SCO = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)


class LSVitrosPlasmaResult(BaseAssayResult):

    class Meta:
        db_table = "assaylsvitros_plasma"

    SCO = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=255, null=False, blank=True)


class GeeniusResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "geenius_row"

    gp36_BI = models.CharField(max_length=255, null=False, blank=True)
    gp140_BI = models.CharField(max_length=255, null=False, blank=True)
    p31_BI = models.CharField(max_length=255, null=False, blank=True)
    gp160_BI = models.CharField(max_length=255, null=False, blank=True)
    p24_BI = models.CharField(max_length=255, null=False, blank=True)
    gp41_BI = models.CharField(max_length=255, null=False, blank=True)
    ctrl_BI = models.CharField(max_length=255, null=False, blank=True)
    GeeniusIndex_reported = models.CharField(max_length=255, null=False, blank=True)
    GeeniusIndex = models.CharField(max_length=255, null=False, blank=True)


class GeeniusResult(BaseAssayResult):

    class Meta:
        db_table = "assaygeenius"

    gp36_BI = models.FloatField(null=True, blank=False)
    gp140_BI = models.FloatField(null=True, blank=False)
    p31_BI = models.FloatField(null=True, blank=False)
    gp160_BI = models.FloatField(null=True, blank=False)
    p24_BI = models.FloatField(null=True, blank=False)
    gp41_BI = models.FloatField(null=True, blank=False)
    ctrl_BI = models.FloatField(null=True, blank=False)
    GeeniusIndex_reported = models.FloatField(null=True, blank=False)
    GeeniusIndex = models.FloatField(null=True, blank=False)


class BEDResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "bed_row"

    OD = models.CharField(max_length=255, null=False, blank=True)
    calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    ODn_reported = models.CharField(max_length=255, null=False, blank=True)
    ODn = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)


class BEDResult(BaseAssayResult):

    class Meta:
        db_table = "assaybed"

    OD = models.FloatField(null=True, blank=False)
    calibrator_OD = models.FloatField(null=True, blank=False)
    ODn_reported = models.FloatField(null=True, blank=False)
    ODn = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=10, null=False, blank=True)



class LuminexCDCResult(BaseAssayResult):

    class Meta:
        db_table = "assayluminexcdc"

    BSA_MFI = models.FloatField(null=True)
    IgG_MFI = models.FloatField(null=True)
    gp120_MFI = models.FloatField(null=True)
    gp160_MFI = models.FloatField(null=True)
    gp41_MFI = models.FloatField(null=True)
    BSA_MFImb = models.FloatField(null=True)
    IgG_MFImb = models.FloatField(null=True)
    gp120_MFImb = models.FloatField(null=True)
    gp160_MFImb = models.FloatField(null=True)
    gp41_MFImb = models.FloatField(null=True)
    calibrator_BSA = models.FloatField(null=True)
    calibrator_IgG = models.FloatField(null=True)
    calibrator_gp120 = models.FloatField(null=True)
    calibrator_gp160 = models.FloatField(null=True)
    calibrator_gp41 = models.FloatField(null=True)
    gp120_MFIn = models.FloatField(null=True)
    gp160_MFIn = models.FloatField(null=True)
    gp41_MFIn = models.FloatField(null=True)
    DEA_treated_BSA_MFI = models.FloatField(null=True)
    DEA_treated_IgG_MFI = models.FloatField(null=True)
    DEA_treated_gp120_MFI = models.FloatField(null=True)
    DEA_treated_gp160_MFI = models.FloatField(null=True)
    DEA_treated_gp41_MFI = models.FloatField(null=True)
    DEA_treated_BSA_MFImb = models.FloatField(null=True)
    DEA_treated_IgG_MFImb = models.FloatField(null=True)
    DEA_treated_gp120_MFImb = models.FloatField(null=True)
    DEA_treated_gp160_MFImb = models.FloatField(null=True)
    DEA_treated_gp41_MFImb = models.FloatField(null=True)
    DEA_treated_gp120_MFIn = models.FloatField(null=True)
    DEA_treated_gp160_MFIn = models.FloatField(null=True)
    DEA_treated_gp41_MFIn = models.FloatField(null=True)
    gp120_AI = models.FloatField(null=True)
    gp160_AI = models.FloatField(null=True)
    gp41_AI = models.FloatField(null=True)
    recent_curtis_2016_alg = models.NullBooleanField(default=None)
    recent_curtis_2013_alg35 = models.NullBooleanField(default=None)
    well_untreated = models.CharField(max_length=10, null=True, blank=False)
    well_treated = models.CharField(max_length=10, null=True, blank=False)



class LuminexCDCResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "luminex_cdc_row"

    BSA_MFI = models.CharField(max_length=255, null=True, blank=False)
    IgG_MFI = models.CharField(max_length=255, null=True, blank=False)
    gp120_MFI = models.CharField(max_length=255, null=True, blank=False)
    gp160_MFI = models.CharField(max_length=255, null=True, blank=False)
    gp41_MFI = models.CharField(max_length=255, null=True, blank=False)
    BSA_MFImb = models.CharField(max_length=255, null=True, blank=False)
    IgG_MFImb = models.CharField(max_length=255, null=True, blank=False)
    gp120_MFImb = models.CharField(max_length=255, null=True, blank=False)
    gp160_MFImb = models.CharField(max_length=255, null=True, blank=False)
    gp41_MFImb = models.CharField(max_length=255, null=True, blank=False)
    calibrator_BSA = models.CharField(max_length=255, null=True, blank=False)
    calibrator_IgG = models.CharField(max_length=255, null=True, blank=False)
    calibrator_gp120 = models.CharField(max_length=255, null=True, blank=False)
    calibrator_gp160 = models.CharField(max_length=255, null=True, blank=False)
    calibrator_gp41 = models.CharField(max_length=255, null=True, blank=False)
    gp120_MFIn = models.CharField(max_length=255, null=True, blank=False)
    gp160_MFIn = models.CharField(max_length=255, null=True, blank=False)
    gp41_MFIn = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_BSA_MFI = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_IgG_MFI = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_gp120_MFI = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_gp160_MFI = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_gp41_MFI = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_BSA_MFImb = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_IgG_MFImb = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_gp120_MFImb = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_gp160_MFImb = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_gp41_MFImb = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_gp120_MFIn = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_gp160_MFIn = models.CharField(max_length=255, null=True, blank=False)
    DEA_treated_gp41_MFIn = models.CharField(max_length=255, null=True, blank=False)
    gp120_AI = models.CharField(max_length=255, null=True, blank=False)
    gp160_AI = models.CharField(max_length=255, null=True, blank=False)
    gp41_AI = models.CharField(max_length=255, null=True, blank=False)
    well_untreated = models.CharField(max_length=10, null=True, blank=False)
    well_treated = models.CharField(max_length=10, null=True, blank=False)
    luminex_result = models.ForeignKey(LuminexCDCResult, null=True, db_index=True)


class IDEV3ResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "ide_v3_row"

    tm_OD = models.CharField(max_length=255, null=False, blank=True)
    v3_OD = models.CharField(max_length=255, null=False, blank=True)
    ratioTM = models.CharField(max_length=255, null=False, blank=True)
    ratioV3 = models.CharField(max_length=255, null=False, blank=True)
    intermediate = models.CharField(max_length=255, null=False, blank=True)
    conclusion = models.CharField(max_length=255, null=False, blank=True)
    conclusion_recalc = models.CharField(max_length=255, null=False, blank=True)


class IDEV3Result(BaseAssayResult):

    class Meta:
        db_table = "assayidev3"

    tm_OD = models.FloatField(null=True, blank=False)
    v3_OD = models.FloatField(null=True, blank=False)
    ratioTM = models.FloatField(null=True, blank=False)
    ratioV3 = models.FloatField(null=True, blank=False)
    intermediate = models.FloatField(null=True, blank=False)
    conclusion = models.FloatField(null=True, blank=False)
    conclusion_recalc = models.FloatField(null=True, blank=False)
