
# encoding: utf-8
from lib.fields import ProtectedForeignKey, OneToOneOrNoneField
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
from world_regions.models import Region

import datetime

logger = logging.getLogger(__name__)

def as_days(tdelta):
    return tdelta.days

class CephiaUser(BaseUser):
    class Meta:
        db_table = "cephia_users"

    def __unicode__(self):
        return "%s" % (self.username)


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

    @property
    def region_name(self):
        return self.region.name


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
        ('aliquot','Aliquot'),
        ('assay','Assay'),
        ('diagnostic_test','Diagnostic Test'),
        ('panel_shipment','Panel Shipment'),
        ('panel_membership','Panel Membership'),
        ('protocol_lookup','Protocol Lookup'),
        ('subject','Subject'),
        ('test_history','Diagnostic Test History'),
        ('test_property','Diagnostic Test Properties'),
        ('transfer_in','Transfer In'),
        ('transfer_out','Transfer Out'),
        ('visit','Visit'),
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

    ep_ddi = models.DateField(null=True, blank=True)
    lp_ddi = models.DateField(null=True, blank=True)
    interval_size = models.IntegerField(null=True, blank=True)
    edsc_days_difference = models.IntegerField(null=True, blank=True)
    eddi = models.DateField(null=True, blank=True)
    recalculate = models.BooleanField(default=False)
    eddi_type = models.CharField(max_length=100, null=False, blank=False)


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
    fiebig_stage_at_firstpos = models.CharField(max_length=10, null=True, blank=False)
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

    @property
    def earliest_visit_date(self):
        return self.visits.order_by('-visit_date').first()


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

    days_since_eddi = models.IntegerField(null=True)
    days_since_ep_ddi = models.IntegerField(null=True)
    days_since_lp_ddi = models.IntegerField(null=True)


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
    vl_reported = models.CharField(max_length=10, null=True, blank=False)
    viral_load = models.IntegerField(null=True, blank=False)
    vl_type = models.CharField(max_length=20, null=True, blank=False)
    vl_detectable = models.NullBooleanField()
    scopevisit_ec = models.CharField(max_length=100, null=True, blank=False)
    pregnant = models.NullBooleanField()
    hepatitis = models.NullBooleanField()
    artificial = models.BooleanField(default=False)
    subject = ProtectedForeignKey(Subject, null=True, blank=True, default=None)
    visit_eddi = ProtectedForeignKey(VisitEDDI, null=True, blank=True)
    treatment_naive = models.BooleanField(default=True)
    on_treatment = models.BooleanField(default=False)
    days_on_art = models.IntegerField(null=True, blank=False)
    first_treatment = models.NullBooleanField()
    history = HistoricalRecords()

    def __unicode__(self):
        return self.subject_label

    def update_visit_detail(self):
        vd = self.visitdetail
        if vd is None:
            vd = VisitDetail(visit=self)
        
        vd.after_aids_diagnosis = self.after_aids_diagnosis
        vd.age_in_years = self.subject.age_in_years
        vd.ever_scope_ec = self.subject.ever_scope_ec(self)
        vd.earliest_visit_date = self.subject.earliest_visit_date
        vd.days_since_cohort_entry = self.days_since_cohort_entry
        vd.days_since_first_art = self.days_since_first_art
        vd.days_since_current_art_init = self.days_since_current_art_init
        vd.days_since_first_art = self.days_since_first_art
        vd.days_from_eddi_to_treatment = self.days_from_eddi_to_treatment
        vd.days_since_first_draw = self.days_since_first_draw
        vd.region = self

    @property
    def age_in_years(self):
        visit_date = self.visit_date
        born = self.subject.date_of_birth
        return visit_date.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def get_region(self):
        pass
        
    @property
    def after_aids_diagnosis(self):
        return bool(self.subject.aids_diagnosis_date and self.visit_date > self.subject.aids_diagnosis_date)

    @property
    def ever_aids_diagnosis(self):
        return bool(self.subject.aids_diagnosis_date)

    @property
    def days_since_cohort_entry(self):
        return as_days(self.visit_date - self.subject.cohort_entry_date)

    @property
    def days_since_first_draw(self):
        return as_days(self.visit_date - self.subject.earliest_visit_date)

    @property
    def days_since_first_art(self):
        # how to handle visit after art
        if self.art_initiation_date > self.visit_date:
            return None
        
        if self.subject.art_initiation_date is not None and self.on_treatment is True:
            return as_days(self.visit_date - subject.art_initiation_date)
        return None

    @property
    def days_since_current_art_init(self):
        if not self.on_treatment:
            return None

        if self.subject.art_resumption_date and self.subject.art_resumption_date < self.visit_date:
            return as_days(self.visit_date - self.subject.art_resumption_date)

        if self.subject.art_initiation_date:
            return as_days(self.visit_date - self.subject.art_initiation_date)

        return None

    @property
    def days_from_eddi_to_current_art(self):
        if self.on_treatment and self.subject.eddi and self.subject.art_initiation_date:
            return as_days(self.subject.eddi.eddi - self.subject.art_initiation_date)
        return None
            
    
class VisitDetail(models.Model):
    visit = OneToOneOrNoneField('Visit', related_name='visitdetail')
    after_aids_diagnosis = models.NullBooleanField()
    age_in_years = models.PositiveIntegerField(null=True)
    ever_aids_diagnosis = models.NullBooleanField()
    ever_scope_ec = models.NullBooleanField()
    earliest_visit_date = models.DateTimeField(null=True)
    days_since_cohort_entry = models.TimeField(null=True)
    days_since_first_draw = models.TimeField(null=True)
    days_since_first_art_visit = models.TimeField(null=True)
    days_from_eddi_to_treatment = models.TimeField(null=True)
    region = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


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



    
