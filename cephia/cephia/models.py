# encoding: utf-8
from lib.fields import ProtectedForeignKey
from django.db import models
from django.conf import settings
import os
from file_handlers.file_handler_register import *
import logging
from django.forms.models import model_to_dict
from simple_history.models import HistoricalRecords
import collections
from user_management.models import BaseUser
from fields import ProtectedForeignKey

logger = logging.getLogger(__name__)

class CephiaUser(BaseUser):
    class Meta:
        db_table = "cephia_users"

    def __unicode__(self):
        return "%s" % (self.username)


class Region(models.Model):

    class Meta:
        db_table = "cephia_regions"

    name = models.CharField(max_length=100, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name


class Country(models.Model):

    class Meta:
        db_table = "cephia_countries"

    code = models.CharField(max_length=5, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    region = ProtectedForeignKey(Region, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.code


class Laboratory(models.Model):
    class Meta:
        db_table = "cephia_laboratories"

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    
    def __unicode__(self):
        return self.name

class Location(models.Model):
    class Meta:
        db_table = "cephia_locations"

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    
    def __unicode__(self):
        return self.name


class Study(models.Model):
    class Meta:
        db_table = "cephia_studies"

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return self.name


class Ethnicity(models.Model):

    class Meta:
        db_table = "cephia_ethnicities"

    name = models.CharField(max_length=30, null=False, blank=False)

class Subtype(models.Model):

    class Meta:
        db_table = "cephia_subtypes"

    name = models.CharField(max_length=30, null=False, blank=False)


class Assay(models.Model):
    class Meta:
        db_table = "cephia_assay"

    name = models.CharField(max_length=255, null=False, blank=False)
    long_name = models.CharField(max_length=255, null=False, blank=False)
    developer = models.CharField(max_length=255, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return "%s" % (self.name)

class SpecimenType(models.Model):

    class Meta:
        db_table = "cephia_specimen_types"

    name = models.CharField(max_length=255, null=False, blank=False)
    spec_type = models.CharField(max_length=10, null=False, blank=False)
    spec_group = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class Panel(models.Model):

    class Meta:
        db_table = "cephia_panels"

    short_name = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=False)
    specimen_type = ProtectedForeignKey(SpecimenType, null=True, blank=False, db_index=True)
    volume = models.FloatField(null=True, blank=True)
    n_recent = models.IntegerField(null=True, blank=False)
    n_longstanding = models.IntegerField(null=True, blank=False)
    n_challenge = models.IntegerField(null=True, blank=False)
    n_reproducibility_controls = models.IntegerField(null=True, blank=False)
    n_negative = models.IntegerField(null=True, blank=False)
    n_total = models.IntegerField(null=True, blank=False)
    blinded = models.NullBooleanField()
    notes = models.TextField(null=True, blank=False)

    def __unicode__(self):
        return self.short_name


class FileInfo(models.Model):

    class Meta:
        db_table = "cephia_datafiles"

    STATE_CHOICES = (
        ('pending','Pending'),
        ('imported','Imported'),
        ('validated','Validated'),
        ('error','Error')
    )

    FILE_TYPE_CHOICES = (
        ('','---------'),
        ('subject','Subject'),
        ('visit','Visit'),
        ('transfer_in','Transfer In'),
        ('aliquot','Aliquot'),
        ('transfer_out','Transfer Out'),
        ('assay','Assay'),
        ('panel_shipment','Panel Shipment'),
        ('panel_membership','Panel Membership'),
        ('diagnostic_test','Diagnostic Test'),
        ('protocol_lookup','Protocol Lookup'),
        ('test_history','Diagnostic Test History'),
        ('test_property','Diagnostic Test Properties'),
    )

    data_file = models.FileField(upload_to=settings.MEDIA_ROOT, null=False, blank=False)
    file_type = models.CharField(max_length=20, null=False, blank=False, choices=FILE_TYPE_CHOICES)
    assay = ProtectedForeignKey(Assay, db_index=True, default=None, null=True)
    panel = ProtectedForeignKey(Panel, db_index=True, default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=10, null=False, blank=False, default='pending')
    priority = models.IntegerField(null=False, blank=False, default=1)
    message = models.TextField(blank=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.data_file.name

    def filename(self):
        return os.path.basename(self.data_file.name)

    def get_handler(self):
        if self.assay:
            return get_file_handler_for_type(self.file_type, self.assay.name)(self)
        else:
            return get_file_handler_for_type(self.file_type, None)(self)

    def get_row(self, row_id):
        if self.file_type == 'subject':
            return SubjectRow.objects.get(fileinfo__id=self.id, id=row_id)
        elif self.file_type == 'visit':
            return VisitRow.objects.get(fileinfo__id=self.id, id=row_id)
        elif self.file_type == 'transfer_in':
            return TransferInRow.objects.get(fileinfo__id=self.id, id=row_id)
        elif self.file_type == 'aliquot':
            return AliquotRow.objects.get(fileinfo__id=self.id, id=row_id)
        elif self.file_type == 'transfer_out':
            return TransferOutRow.objects.get(fileinfo__id=self.id, id=row_id)
        elif self.file_type == 'panel_membership':
            return PanelMembershipRow.objects.get(fileinfo__id=self.id, id=row_id)
        elif self.file_type == 'panel_shipment':
            return PanelShipmentRow.objects.get(fileinfo__id=self.id, id=row_id)
        elif self.file_type == 'assay':
            if self.assay.name == 'lag':
                return LagResultRow.objects.get(fileinfo__id=self.id, id=row_id)
            elif self.assay.name == 'biorad':
                return BioradResultRow.objects.get(fileinfo__id=self.id, id=row_id)

    def get_extension(self):
        return self.filename().split('.')[-1]


class ImportedRow(models.Model):
    class Meta:
        abstract = True
    
    STATE_CHOICES = (
        ('pending','Pending'),
        ('validated','Validated'),
        ('imported','Imported'),
        ('processed','Processed'),
        ('error','Error')
    )

    state = models.CharField(max_length=10, choices=STATE_CHOICES, null=False, blank=False)
    error_message = models.TextField(blank=True)
    date_processed = models.DateTimeField(auto_now_add=True)
    fileinfo = ProtectedForeignKey(FileInfo, db_index=True)
    history = HistoricalRecords()

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


class ImportedRowComment(models.Model):

    class Meta:
        db_table = "cephia_importedrow_comments"

    comment = models.TextField(blank=False, null=False)
    resolve_date = models.DateTimeField(blank=False, null=False)
    resolve_action = models.TextField(blank=False, null=False)
    assigned_to = models.CharField(max_length=50, null=False, blank=False)

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


class SubjectEDDI(models.Model):
    class Meta:
        db_table = "cephia_subject_eddi"
        
    tci_begin = models.DateField(null=True, blank=True)
    tci_end = models.DateField(null=True, blank=True)
    tci_size = models.IntegerField(null=True, blank=True)
    edsc_days_difference = models.IntegerField(null=True, blank=True)
    eddi = models.DateField(null=True, blank=True)
    recalculate = models.BooleanField(default=False)


class SubjectEDDIStatus(models.Model):
    class Meta:
        db_table = "cephia_subject_eddi_status"

    STATUS_CHOICES = (
        ('ok','OK'),
        ('investigate','Investigate'),
        ('suspected_incorrect_data','Suspected Incorrect Data'),
        ('resolved','Resolved'),
        ('other','Other'),
    )

    status = models.CharField(max_length=30, null=True, blank=False, choices=STATUS_CHOICES)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


class Subject(models.Model):

    class Meta:
        db_table = "cephia_subjects"

    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female'),
        ('unkown','Unkown')
    )

    STATUS_CHOICES = (
        ('negative','Negative'),
        ('positive','Positive'),
    )
    
    subject_label = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    cohort_entry_date = models.DateField(null=True, blank=True, db_index=True)
    cohort_entry_hiv_status = models.CharField(max_length=8, null=False, blank=False, choices=STATUS_CHOICES)
    country = ProtectedForeignKey(Country, null=True, blank=True)
    last_negative_date = models.DateField(null=True, blank=True)
    first_positive_date = models.DateField(null=True, blank=True)
    edsc_reported  = models.DateField(null=True, blank=True, default=None)
    ars_onset_date = models.DateField(null=True, blank=True)
    fiebig_stage_at_firstpos = models.CharField(max_length=10, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=6, null=False, blank=True, choices=GENDER_CHOICES)
    transgender = models.NullBooleanField()
    population_group = ProtectedForeignKey(Ethnicity, null=True, blank=True)
    risk_sex_with_men = models.NullBooleanField()
    risk_sex_with_women = models.NullBooleanField()
    risk_idu = models.NullBooleanField()
    subtype_confirmed = models.NullBooleanField()
    subtype = ProtectedForeignKey(Subtype, null=True, blank=True, db_index=True)
    art_initiation_date = models.DateField(null=True, blank=True)
    aids_diagnosis_date = models.DateField(null=True, blank=True)
    art_interruption_date = models.DateField(null=True, blank=True)
    art_resumption_date = models.DateField(null=True, blank=True)
    artificial = models.BooleanField(default=False)
    source_study = ProtectedForeignKey(Study, null=True, blank=True)
    subject_eddi = ProtectedForeignKey(SubjectEDDI, null=True, blank=True)
    subject_eddi_status = ProtectedForeignKey(SubjectEDDIStatus, null=True, blank=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.subject_label


class SubjectRow(ImportedRow):

    class Meta:
        db_table = "cephia_subjectrows"

    subject_label = models.CharField(max_length=255, null=False, blank=True)
    source_study = models.CharField(max_length=255, null=False, blank=True)
    cohort_entry_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    cohort_entry_date_mm = models.CharField(max_length=255, null=False, blank=True)
    cohort_entry_date_dd = models.CharField(max_length=255, null=False, blank=True)
    cohort_entry_hiv_status = models.CharField(max_length=255, null=False, blank=True)
    country = models.CharField(max_length=255, null=False, blank=True)
    last_negative_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    last_negative_date_mm = models.CharField(max_length=255, null=False, blank=True)
    last_negative_date_dd = models.CharField(max_length=255, null=False, blank=True)
    first_positive_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    first_positive_date_mm = models.CharField(max_length=255, null=False, blank=True)
    first_positive_date_dd = models.CharField(max_length=255, null=False, blank=True)
    edsc_reported_yyyy = models.CharField(max_length=255, null=False, blank=True)
    edsc_reported_mm = models.CharField(max_length=255, null=False, blank=True)
    edsc_reported_dd = models.CharField(max_length=255, null=False, blank=True)
    fiebig_stage_at_firstpos = models.CharField(max_length=255, null=False, blank=True)
    ars_onset_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    ars_onset_date_mm = models.CharField(max_length=255, null=False, blank=True)
    ars_onset_date_dd = models.CharField(max_length=255, null=False, blank=True)
    date_of_birth_yyyy = models.CharField(max_length=255, null=False, blank=True)
    date_of_birth_mm = models.CharField(max_length=255, null=False, blank=True)
    date_of_birth_dd = models.CharField(max_length=255, null=False, blank=True)
    sex = models.CharField(max_length=255, null=False, blank=True)
    transgender = models.CharField(max_length=255, null=False, blank=True)
    population_group = models.CharField(max_length=255, null=False, blank=True)
    risk_sex_with_men = models.CharField(max_length=255, null=False, blank=True)
    risk_sex_with_women = models.CharField(max_length=255, null=False, blank=True)
    risk_idu = models.CharField(max_length=255, null=False, blank=True)
    subtype = models.CharField(max_length=255, null=False, blank=True)
    subtype_confirmed = models.CharField(max_length=255, null=False, blank=True)
    aids_diagnosis_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    aids_diagnosis_date_mm = models.CharField(max_length=255, null=False, blank=True)
    aids_diagnosis_date_dd = models.CharField(max_length=255, null=False, blank=True)
    art_initiation_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    art_initiation_date_mm = models.CharField(max_length=255, null=False, blank=True)
    art_initiation_date_dd = models.CharField(max_length=255, null=False, blank=True)
    art_interruption_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    art_interruption_date_mm = models.CharField(max_length=255, null=False, blank=True)
    art_interruption_date_dd = models.CharField(max_length=255, null=False, blank=True)
    art_resumption_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    art_resumption_date_mm = models.CharField(max_length=255, null=False, blank=True)
    art_resumption_date_dd = models.CharField(max_length=255, null=False, blank=True)
    comment = ProtectedForeignKey(ImportedRowComment, blank=False, null=True)
    subject = ProtectedForeignKey(Subject, null=True, blank=False)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.subject_label


class VisitEDDI(models.Model):
    class Meta:
        db_table = "cephia_visit_eddi"
        
    tci_begin = models.DateField(null=True, blank=True)
    tci_end = models.DateField(null=True, blank=True)
    eddi = models.DateField(null=True, blank=True)


class Visit(models.Model):

    class Meta:
        db_table = "cephia_visits"

    STATUS_CHOICES = (
        ('negative','Negative'),
        ('positive','Positive'),
        ('unknown','Unkown'),
    )
    
    subject_label = models.CharField(max_length=255, null=False, blank=False)
    visit_date = models.DateField(null=True, blank=True)
    visit_hivstatus = models.CharField(max_length=8, null=False, blank=False, choices=STATUS_CHOICES)
    source_study = ProtectedForeignKey(Study, null=True, blank=True)
    cd4_count = models.IntegerField(null=True, blank=False)
    vl = models.CharField(max_length=10, null=True, blank=False)
    scopevisit_ec = models.CharField(max_length=100, null=True, blank=False)
    pregnant = models.NullBooleanField()
    hepatitis = models.NullBooleanField()
    artificial = models.BooleanField(default=False)
    subject = ProtectedForeignKey(Subject, null=True, blank=True, default=None)
    visit_eddi = ProtectedForeignKey(VisitEDDI, null=True, blank=True)
    treatment_naive = models.NullBooleanField()
    on_treatment = models.NullBooleanField()
    history = HistoricalRecords()

    def __unicode__(self):
        return self.subject_label


class VisitRow(ImportedRow):

    class Meta:
        db_table = "cephia_visitrows"

    subject_label = models.CharField(max_length=255, null=False, blank=True)
    visitdate_yyyy = models.CharField(max_length=255, null=False, blank=True)
    visitdate_mm = models.CharField(max_length=255, null=False, blank=True)
    visitdate_dd = models.CharField(max_length=255, null=False, blank=True)
    visit_hivstatus = models.CharField(max_length=255, null=False, blank=True)
    source_study = models.CharField(max_length=255, null=False, blank=True)
    cd4_count = models.CharField(max_length=255, null=False, blank=True)
    vl = models.CharField(max_length=255, null=False, blank=True)
    artificial = models.CharField(max_length=255, null=False, blank=True)
    scopevisit_ec = models.CharField(max_length=255, null=False, blank=True)
    pregnant = models.CharField(max_length=255, null=False, blank=True)
    hepatitis = models.CharField(max_length=255, null=False, blank=True)
    comment = ProtectedForeignKey(ImportedRowComment, blank=False, null=True)
    visit = ProtectedForeignKey(Visit, null=True, blank=False)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.subject_label





class Specimen(models.Model):

    VISIT_LINKAGE_CHOICES = (
        ('provisional','Provisional'),
        ('confirmed','Confirmed'),
        ('artificial','Artificial'),
    )

    class Meta:
        db_table = "cephia_specimens"

    specimen_label = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    parent_label = models.CharField(max_length=255, null=True, blank=True)
    subject_label = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    number_of_containers = models.IntegerField(null=True, blank=True)
    reported_draw_date = models.DateField(null=True, blank=True)
    transfer_in_date = models.DateField(null=True, blank=True)
    transfer_out_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    modified_date = models.DateField(null=True, blank=True)
    transfer_reason = models.CharField(max_length=50, null=True, blank=True)
    subject = ProtectedForeignKey(Subject, null=True, blank=False)
    visit = ProtectedForeignKey(Visit, null=True, blank=False, related_name='visit')
    visit_linkage = models.CharField(max_length=12, null=True, blank=False, choices=VISIT_LINKAGE_CHOICES)
    specimen_type = ProtectedForeignKey(SpecimenType, null=True, blank=True, db_index=True)
    volume = models.FloatField(null=True, blank=True)
    volume_units = models.CharField(max_length=20, null=True, blank=True)
    initial_claimed_volume = models.FloatField(null=True, blank=True)
    source_study = ProtectedForeignKey(Study, null=True, blank=True)
    shipped_to = ProtectedForeignKey(Laboratory, related_name='shipped_to', null=True, blank=True)
    shipped_in_panel = models.CharField(max_length=255, null=True, blank=True)
    location = ProtectedForeignKey(Location, null=True, blank=True)
    parent = ProtectedForeignKey('Specimen', null=True, blank=False, default=None)
    aliquoting_reason = models.CharField(max_length=20, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    history = HistoricalRecords()


    def __unicode__(self):
        return self.specimen_label

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


class TransferInRow(ImportedRow):

    class Meta:
        db_table = "cephia_transfer_in_rows"

    specimen_label = models.CharField(max_length=255, null=True, blank=True)
    subject_label = models.CharField(max_length=255, null=True, blank=True)
    drawdate_yyyy = models.CharField(max_length=255, null=True, blank=True)
    drawdate_mm = models.CharField(max_length=255, null=True, blank=True)
    drawdate_dd = models.CharField(max_length=255, null=True, blank=True)
    number_of_containers = models.CharField(max_length=255, null=True, blank=True)
    transfer_date_yyyy = models.CharField(max_length=255, null=True, blank=True)
    transfer_date_mm = models.CharField(max_length=255, null=True, blank=True)
    transfer_date_dd = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    transfer_reason = models.CharField(max_length=255, null=True, blank=True)
    specimen_type = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    volume_units = models.CharField(max_length=255, null=True, blank=True)
    source_study = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    comment = ProtectedForeignKey(ImportedRowComment, blank=False, null=True)
    specimen = ProtectedForeignKey(Specimen, null=True, blank=False)
    roll_up = models.NullBooleanField()
    history = HistoricalRecords()


    def __unicode__(self):
        return self.specimen_label


class TransferOutRow(ImportedRow):

    class Meta:
        db_table = "cephia_transfer_out_rows"
        
    specimen_label = models.CharField(max_length=255, null=True, blank=True) 
    number_of_containers = models.CharField(max_length=255, null=True, blank=True)
    specimen_type = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    volume_units = models.CharField(max_length=255, null=True, blank=True)
    shipped_in_panel = models.CharField(max_length=255, null=True, blank=True)
    shipment_date_dd = models.CharField(max_length=255, null=True, blank=True)
    shipment_date_mm = models.CharField(max_length=255, null=True, blank=True)
    shipment_date_yyyy = models.CharField(max_length=255, null=True, blank=True)
    destination_site = models.CharField(max_length=255, null=True, blank=True)
    comment = ProtectedForeignKey(ImportedRowComment, blank=False, null=True)
    specimen = ProtectedForeignKey(Specimen, null=True, blank=False)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.specimen_label


class AliquotRow(ImportedRow):

    class Meta:
        db_table = "cephia_aliquot_rows"
        
    parent_label = models.CharField(max_length=255, null=True, blank=True, db_index=True) 
    aliquot_label = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    volume_units = models.CharField(max_length=255, null=True, blank=True)
    number_of_aliquot = models.CharField(max_length=255, null=True, blank=True)
    aliquoting_date_yyyy = models.CharField(max_length=255, null=True, blank=True)
    aliquoting_date_mm = models.CharField(max_length=255, null=True, blank=True)
    aliquoting_date_dd = models.CharField(max_length=255, null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    specimen_type = models.CharField(max_length=255, null=True, blank=True)
    comment = ProtectedForeignKey(ImportedRowComment, blank=False, null=True)
    specimen = ProtectedForeignKey(Specimen, null=True, blank=False, db_index=True)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.parent_label
