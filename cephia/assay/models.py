# encoding: utf-8
from django.db import models
from cephia.models import (Visit, Specimen, SpecimenType, ImportedRow,
                           Assay, Laboratory, Panel, FileInfo)
from lib.fields import ProtectedForeignKey
from lib import log_exception
from assay_result_factory import *
from django.forms.models import model_to_dict
import logging
import math

logger = logging.getLogger(__name__)

INTEPRETATIONS = [
        ('recent', 'Recent'),
        ('non_recent', 'Non-Recent')
    ]

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
    interpretation = models.CharField(choices=INTEPRETATIONS, max_length=255, null=True, blank=False)

    def __unicode__(self):
        return self.specimen.specimen_label

    def get_results_for_run(self):
        if self.assay:
            headers = ['result']
            results = [ result for result in AssayResult.objects.filter(assay_run=self.assay_run) ]
            return headers, results

        return None

    def get_specific_results(self):
        if self.assay:
            result_model = get_result_model(self.assay.name)
            headers = result_model._meta.get_all_field_names()
            results = [ result.model_to_dict() for result in result_model.objects.filter(assay_result=self) ]
            return headers, results

        return None

    def get_specific_results_for_run(self):
        if self.assay:
            result_model = get_result_model(self.assay.name)
            parent_fields = BaseAssayResult._meta.get_all_field_names()
            child_fields = result_model._meta.get_all_field_names()
            local_fields = list(set(child_fields)-set(parent_fields))
            headers = [ header for header in local_fields if header != 'id']
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
    interpretation = models.CharField(choices=INTEPRETATIONS, max_length=255, null=True, blank=False)
    exclusion = models.CharField(max_length=255, null=True, blank=False)
    warning_msg = models.CharField(max_length=255, null=True, blank=False)
    error_message = models.CharField(max_length=255, null=True, blank=False)

    def save(self, *args, **kwargs):
        for field in self._meta.get_all_field_names():
            field_type = self._meta.get_field(field)
            if not field_type.one_to_many and not field_type.related_model:
                if getattr(self, field) == 'NA' and field_type.get_internal_type() == 'FloatField':
                    setattr(self, field, None)
                if getattr(self, field) == 'NEG' and field_type.get_internal_type() == 'FloatField':
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



class LagSediaResult(BaseAssayResult):

    class Meta:
        db_table = "assay_lagsedia"

    OD = models.FloatField(null=True, blank=False)
    calibrator_OD = models.FloatField(null=True, blank=False)
    ODn = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=10, null=False, blank=True)

    def __unicode__(self):
        return self.specimen


class LagSediaResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_lagsedia_row"

    OD = models.CharField(max_length=255, null=False, blank=True)
    calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    ODn = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)
    lag_sedia_result = models.ForeignKey(LagSediaResult, null=True, blank=False, db_index=True)


    def __unicode__(self):
        return self.specimen_label


class LagMaximResult(BaseAssayResult):

    class Meta:
        db_table = "assay_lagmaxim"

    OD = models.FloatField(null=True, blank=False)
    calibrator_OD = models.FloatField(null=True, blank=False)
    ODn = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=10, null=False, blank=True)

    def __unicode__(self):
        return self.specimen.specimen_label


class LagMaximResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_lagmaxim_row"

    OD = models.CharField(max_length=255, null=False, blank=True)
    calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    ODn = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)
    lag_maxim_result = models.ForeignKey(LagMaximResult, null=True, blank=False, db_index=True)

    def __unicode__(self):
        return self.specimen_label


class ArchitectUnmodifiedResult(BaseAssayResult):

    class Meta:
        db_table = "assay_architect_unmodified"

    SCO = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=255, null=True, blank=True)


class ArchitectUnmodifiedResultRow(BaseAssayResultRow):
    class Meta:
        db_table = "assay_architect_unmodified_row"

    SCO = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)
    architect_unmodified_result = models.ForeignKey(ArchitectUnmodifiedResult, null=True, blank=False, db_index=True)


class ArchitectAvidityResult(BaseAssayResult):

    class Meta:
        db_table = "assay_architect_avidity"

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


class ArchitectAvidityResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_architect_avidity_row"

    treated_guanidine_SCO = models.CharField(max_length=255, null=False, blank=True)
    untreated_pbs_SCO = models.CharField(max_length=255, null=False, blank=True)
    AI = models.CharField(max_length=255, null=False, blank=True)
    AI_reported = models.CharField(max_length=255, null=False, blank=True)
    well_treated_guanidine = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_pbs = models.CharField(max_length=255, null=False, blank=True)
    architect_avidity_result = models.ForeignKey(ArchitectAvidityResult, null=True, blank=False, db_index=True)


class BioRadAvidityCDCResult(BaseAssayResult):

    class Meta:
        db_table = "assay_biorad_avidity_cdc"

    treated_DEA_OD = models.FloatField(null=True)
    untreated_dilwashsoln_OD = models.FloatField(null=True)
    AI_reported = models.FloatField(null=True)
    AI = models.FloatField(null=True)
    well_treated_DEA = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_dilwashsoln = models.CharField(max_length=255, null=False, blank=True)


class BioRadAvidityCDCResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_biorad_avidity_cdc_row"

    treated_DEA_OD = models.CharField(max_length=255, null=False, blank=True)
    untreated_dilwashsoln_OD = models.CharField(max_length=255, null=False, blank=True)
    AI_reported = models.CharField(max_length=255, null=False, blank=True)
    AI = models.CharField(max_length=255, null=False, blank=True)
    well_treated_DEA = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_dilwashsoln = models.CharField(max_length=255, null=False, blank=True)
    biorad_avidity_cdc_result = models.ForeignKey(BioRadAvidityCDCResult, null=True, blank=False, db_index=True)


class BioRadAvidityJHUResult(BaseAssayResult):
    class Meta:
        db_table = "assay_biorad_avidity_jhu"

    treated_DEA_OD = models.FloatField(null=True, blank=False)
    untreated_dilwashsoln_OD = models.FloatField(null=True, blank=False)
    AI_reported = models.FloatField(null=True, blank=False)
    AI = models.FloatField(null=True, blank=False)
    well_treated_DEA = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_dilwashsoln = models.CharField(max_length=255, null=False, blank=True)


class BioRadAvidityJHUResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_biorad_avidity_jhu_row"

    treated_DEA_OD = models.CharField(max_length=255, null=False, blank=True)
    untreated_dilwashsoln_OD = models.CharField(max_length=255, null=False, blank=True)
    AI_reported = models.CharField(max_length=255, null=False, blank=True)
    AI = models.CharField(max_length=255, null=False, blank=True)
    well_treated_DEA = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_dilwashsoln = models.CharField(max_length=255, null=False, blank=True)
    biorad_avidity_jhu_result = models.ForeignKey(BioRadAvidityJHUResult, null=True, blank=False, db_index=True)


class BioRadAvidityGlasgowResult(BaseAssayResult):
    class Meta:
        db_table = "assay_biorad_avidity_glasgow"

    treated_urea_OD = models.FloatField(null=True, blank=False)
    untreated_buffer_OD = models.FloatField(null=True, blank=False)
    AI_reported = models.FloatField(null=True, blank=False)
    AI = models.FloatField(null=True, blank=False)
    well_treated_urea = models.CharField(max_length=255, null=True, blank=False)
    well_untreated_buffer = models.CharField(max_length=255, null=True, blank=False)
    dilution = models.CharField(max_length=255, null=True, blank=False)


class BioRadAvidityGlasgowResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_biorad_avidity_glasgow_row"

    treated_urea_OD = models.CharField(max_length=255, null=True, blank=False)
    untreated_buffer_OD = models.CharField(max_length=255, null=True, blank=False)
    AI_reported = models.CharField(max_length=255, null=True, blank=False)
    AI = models.CharField(max_length=255, null=True, blank=False)
    well_treated_urea = models.CharField(max_length=255, null=True, blank=False)
    well_untreated_buffer = models.CharField(max_length=255, null=True, blank=False)
    dilution = models.CharField(max_length=255, null=True, blank=False)
    biorad_avidity_glasgow_result = models.ForeignKey(BioRadAvidityGlasgowResult, null=True, blank=False, db_index=True)


class VitrosAvidityResult(BaseAssayResult):

    class Meta:
        db_table = "assay_vitros_avidity"

    treated_guanidine_OD = models.FloatField(max_length=255, null=True)
    untreated_pbs_OD = models.FloatField(max_length=255, null=True)
    AI = models.FloatField(max_length=255, null=True)
    AI_reported = models.FloatField(max_length=255, null=True)
    well_treated_guanidine = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_pbs = models.CharField(max_length=255, null=False, blank=True)


class VitrosAvidityResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_vitros_avidity_row"

    treated_guanidine_OD = models.CharField(max_length=255, null=False, blank=True)
    untreated_pbs_OD = models.CharField(max_length=255, null=False, blank=True)
    AI = models.CharField(max_length=255, null=False, blank=True)
    AI_reported = models.CharField(max_length=255, null=False, blank=True)
    well_treated_guanidine = models.CharField(max_length=255, null=False, blank=True)
    well_untreated_pbs = models.CharField(max_length=255, null=False, blank=True)
    vitros_avidity_result = models.ForeignKey(VitrosAvidityResult, null=True, blank=False, db_index=True)


class LSVitrosDiluentResult(BaseAssayResult):

    class Meta:
        db_table = "assay_lsvitros_diluent"

    SCO = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=10, null=False, blank=True)


class LSVitrosDiluentResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_lsvitros_diluent_row"

    SCO = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)
    lsvitros_diluent_result = models.ForeignKey(LSVitrosDiluentResult, null=True, blank=False, db_index=True)


class LSVitrosPlasmaResult(BaseAssayResult):

    class Meta:
        db_table = "assay_lsvitros_plasma"

    SCO = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=255, null=False, blank=True)


class LSVitrosPlasmaResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_lsvitros_plasma_row"

    SCO = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)
    lsvitros_diluent_result = models.ForeignKey(LSVitrosDiluentResult, null=True, blank=False, db_index=True)


class GeeniusResult(BaseAssayResult):

    class Meta:
        db_table = "assay_geenius"

    gp36_bi = models.FloatField(null=True, blank=True)
    gp140_bi = models.FloatField(null=True)
    p31_bi = models.FloatField(null=True)
    gp160_bi = models.FloatField(null=True)
    p24_bi = models.FloatField(null=True)
    gp41_bi = models.FloatField(null=True)
    ctrl_bi = models.FloatField(null=True)
    GeeniusIndex = models.FloatField(null=True)
    GeeniusIndex_reported = models.FloatField(null=True, blank=False)


class GeeniusResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_geenius_row"

    gp36_bi = models.CharField(max_length=255, null=True, blank=True)
    gp140_bi = models.CharField(max_length=255, null=True)
    p31_bi = models.CharField(max_length=255, null=True)
    gp160_bi = models.CharField(max_length=255, null=True)
    p24_bi = models.CharField(max_length=255, null=True)
    gp41_bi = models.CharField(max_length=255, null=True)
    ctrl_bi = models.CharField(max_length=255, null=True)
    GeeniusIndex = models.CharField(max_length=255, null=True)
    
    geenius_result = models.ForeignKey(GeeniusResult, null=True, blank=False, db_index=True)


class BEDResult(BaseAssayResult):

    class Meta:
        db_table = "assay_bed"

    OD = models.FloatField(null=True, blank=False)
    calibrator_OD = models.FloatField(null=True, blank=False)
    ODn_reported = models.FloatField(null=True, blank=False)
    ODn = models.FloatField(null=True, blank=False)
    well= models.CharField(max_length=10, null=False, blank=True)


class BEDResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_bed_row"

    OD = models.CharField(max_length=255, null=False, blank=True)
    calibrator_OD = models.CharField(max_length=255, null=False, blank=True)
    ODn_reported = models.CharField(max_length=255, null=False, blank=True)
    ODn = models.CharField(max_length=255, null=False, blank=True)
    well= models.CharField(max_length=255, null=False, blank=True)
    bed_result = models.ForeignKey(BEDResult, null=True, blank=False, db_index=True)


class LuminexCDCResult(BaseAssayResult):

    class Meta:
        db_table = "assay_luminex_cdc"

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
        db_table = "assay_luminex_cdc_row"

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


class IDEV3Result(BaseAssayResult):

    class Meta:
        db_table = "assay_idev3"

    well_tm = models.CharField(max_length=10, null=True)
    well_v3 = models.CharField(max_length=10, null=True)
    tm_OD = models.FloatField(null=True)
    v3_OD = models.FloatField(null=True)
    tm_ratio_reported = models.FloatField(null=True)
    v3_ratio_reported = models.FloatField(null=True)
    tm_ratio = models.FloatField(null=True)
    v3_ratio = models.FloatField(null=True)
    intermediaire_reported = models.FloatField(null=True)
    intermediaire = models.FloatField(null=True)
    conclusion_reported = models.FloatField(null=True)
    conclusion = models.FloatField(null=True)

    def calculate_and_save(self):
        try:
            if self.tm_OD is not None:
                self.tm_ratio = self.tm_OD / 0.05

            if self.v3_OD is not None:
                self.v3_ratio = self.v3_OD / 0.05

            if self.tm_OD is None or self.v3_OD is None:
                self.intermediaire = None
                self.conclusion = None
                self.interpretation = None
            else:
                # numbers are arbitrary as per the SOP
                self.intermediare = -3.8565 + (0.09502 * self.tm_ratio) +  (0.0379 * self.v3_ratio)
                self.conclusion = math.exp(self.intermediaire) / (1 + math.exp(self.intermediaire))
                self.interpretation = 'recent'  if self.conclusion < 0.5 else 'non_recent'
        except Exception, e:
            self.warning_msg = "Unable to calculate final result: " + log_exception(e, logger)
        finally:
            self.save()
            
class IDEV3ResultRow(BaseAssayResultRow):

    class Meta:
        db_table = "assay_idev3_row"


    well_tm = models.CharField(max_length=255, null=False, blank=True)
    well_v3 = models.CharField(max_length=255)
    tm_OD = models.CharField(max_length=255)
    v3_OD = models.CharField(max_length=255)
    tm_ratio_reported = models.CharField(max_length=255)
    v3_ratio_reported = models.CharField(max_length=255)
    tm_ratio = models.CharField(max_length=255)
    v3_ratio = models.CharField(max_length=255)
    intermediaire_reported = models.CharField(max_length=255)
    intermediaire = models.CharField(max_length=255)
    conclusion_reported = models.CharField(max_length=255)
    conclusion = models.CharField(max_length=255)
    
