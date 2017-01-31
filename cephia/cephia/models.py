
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
from world_regions import models as wr_models
from django.db.models import QuerySet
from django.db.models.functions import Length, Substr, Lower
from django.contrib.auth.models import Group
from dateutil.relativedelta import relativedelta
from lib.email_context_helper import update_email_context
from mailqueue.mailqueue_helper import queue_email, queue_templated_email
import uuid
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
import datetime
import random

logger = logging.getLogger(__name__)

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
    ('viral_load','Viral Load'),
    ('treatment_status_update','Treatment Status Update'),
)

def as_days(tdelta):
    return tdelta.days

def random_string():
    unique_number = False
    while unique_number == False:
        random_number = str(random.randint(10000000, 99999999))
        try:
            Subject.objects.get(subject_label_blinded=random_number)
        except Subject.DoesNotExist:
            unique_number = True
            return str(random.randint(10000000, 99999999))

class CephiaUser(BaseUser):
    
    password_reset_token = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    
    class Meta:
        db_table = "cephia_users"
        permissions = [
            ('can_upload_panel_data', 'Can upload memberships and shipments'),
            ('can_upload_results', 'Can upload results'),
            ('can_upload_clinical_data', 'Can upload subjects and visits'),
            ('can_upload_eddi_data', 'Can upload diagnostic data'),
            ('can_upload_specimen_data', 'Can upload aliquot, transfer in, transfer out'),
            ('can_purge_assay_results', 'Can purge assay results'),
            ('can_purge_assay_runs', 'Can purge assay runs'),
        ]

    def __unicode__(self):
        return "%s" % (self.username)

    @property
    def allowed_file_uploads(self):
        choices = dict(FILE_TYPE_CHOICES)
        permissions = {
            'can_upload_panel_data': ['panel_membership', 'panel_shipment'],
            'can_upload_results': ['assay'],
            'can_upload_clinical_data': ['subject', 'visit', 'viral_load', 'treatment_status_update'],
            'can_upload_specimen_data': ['aliquot', 'transfer_in', 'transfer_out'],
            'can_upload_eddi_data': ['diagnostic_test', 'protocol_lookup', 'test_history',
                                     'test_property']
        }

        allowed = []
        
        for perm, options in permissions.iteritems():
            if self.has_perm('cephia.' + perm):
                allowed.extend((option,choices[option]) for option in options)

        return sorted(allowed)

    @classmethod
    def generate_password_reset_link(self, user):
        """ create an password authentication token for this user """
        token = str(uuid.uuid4()).replace("-","").replace("_","")
        user.password_reset_token = token
        user.save()

    def send_registration_notification(self):
        email_context = {}
        email_context['user'] = self.username
        email_context['link_home'] = settings.SITE_BASE_URL
        email_context = update_email_context(email_context)

        if not self.has_usable_password():
            CephiaUser.generate_password_reset_link(self)
            email_context['link_home'] = u'%s%s' % (settings.BASE_URL,
                                                    reverse('outside_eddi:finalise_user_account',
                                                    kwargs={'token': self.password_reset_token}))

        queue_templated_email(request=None, context=email_context,
                              subject_template="Welcome to the Cephia Infection Dating Tool",
                              text_template='outside_eddi/emails/signup.txt',
                              html_template='outside_eddi/emails/new_member.html',
                              to_addresses=[self.email],
                              bcc_addresses=settings.BCC_EMAILS or [],
                              from_address=settings.FROM_EMAIL)


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
    region = ProtectedForeignKey('Region', null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.code

    @property
    def region_name(self):
        try:
            return wr_models.Region.objects.get(countries__country=self.code).name
        except wr_models.Region.DoesNotExist:
            return None


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
    is_custom = models.BooleanField(null=False, blank=False, default=False)
    created_by = ProtectedForeignKey('cephia.CephiaUser', null=True, related_name='assays')

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
    visits = models.ManyToManyField('Visit', through='assay.PanelMembership', related_name='panels')

    def __unicode__(self):
        return self.short_name or self.name


class FileInfo(models.Model):

    class Meta:
        db_table = "cephia_datafiles"

    STATE_CHOICES = (
        ('pending','Pending'),
        ('imported','Imported'),
        ('validated','Validated'),
        ('error','Error')
    )

    

    SPECIMEN_LABEL_TYPES = [
        ('aliquot_label', 'Aliquot Label'),
        ('root_specimen', 'Root Specimen'),
        ('aliquot_base', 'Aliquot Base'),
    ]

    data_file = models.FileField(upload_to=settings.MEDIA_ROOT, null=False, blank=False)
    file_type = models.CharField(max_length=50, null=False, blank=False, choices=FILE_TYPE_CHOICES)
    assay = ProtectedForeignKey(Assay, db_index=True, default=None, null=True)
    panel = ProtectedForeignKey(Panel, db_index=True, default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=10, null=False, blank=False, default='pending')
    priority = models.IntegerField(null=False, blank=False, default=1)
    message = models.TextField(blank=True)
    history = HistoricalRecords()
    task_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    specimen_label_type = models.CharField(max_length=255, choices=SPECIMEN_LABEL_TYPES, blank=True, default='aliquot_label')

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
        if self.file_type == 'viral_load':
            return ViralLoadRow.objects.get(fileinfo__id=self.id, id=row_id)
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
        ('recalled', 'Recalled'),
        ('pending','Pending'),
        ('validated','Validated'),
        ('imported','Imported'),
        ('processed','Processed'),
        ('error','Error')
    )

    state = models.CharField(max_length=20, choices=STATE_CHOICES, null=False, blank=False)
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
    history = HistoricalRecords()

    @property
    def eddi_interval_size(self):
        return self.interval_size


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
    # subject_label_blinded = models.CharField(max_length=25, null=False, blank=False, default = random_string, unique = True, db_index=True)

    def __unicode__(self):
        return self.subject_label

    @property
    def earliest_visit_date(self):
        v = self.visit_set.order_by('visit_date').first()
        return v.visit_date if v else None


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

    history = HistoricalRecords()
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
    
    vl_reported = models.CharField(max_length=20, null=True, blank=False)
    vl_cephia = models.CharField(max_length=20, null=True, blank=False)

    viral_load = models.IntegerField(null=True, blank=False)
    vl_type = models.CharField(max_length=20, null=True, blank=False)
    vl_detectable = models.NullBooleanField()
    viral_load_offset = models.IntegerField(null=True, default=None)

    scopevisit_ec = models.BooleanField(default=False)
    pregnant = models.NullBooleanField()
    hepatitis = models.NullBooleanField()
    artificial = models.BooleanField(default=False)
    subject = ProtectedForeignKey(Subject, null=True, blank=True, default=None)
    visit_eddi = ProtectedForeignKey(VisitEDDI, null=True, blank=True)
    treatment_naive = models.BooleanField(default=True)
    on_treatment = models.BooleanField(default=False)
    first_treatment = models.NullBooleanField()
    history = HistoricalRecords()

    def __unicode__(self):
        return self.subject_label

    def update_visit_detail(self):
        vd = self.visitdetail
        if vd is None:
            vd = VisitDetail(visit=self)
        
        vd.age_in_years = self.age_in_years
        vd.earliest_visit_date = self.subject.earliest_visit_date
        vd.ever_scope_ec = self.ever_scope_ec
        vd.is_after_aids_diagnosis = self.is_after_aids_diagnosis
        vd.ever_aids_diagnosis = self.ever_aids_diagnosis
        vd.days_since_cohort_entry = self.days_since_cohort_entry
        vd.days_since_first_draw = self.days_since_first_draw
        vd.days_since_first_art = self.days_since_first_art
        vd.days_since_current_art = self.days_since_current_art
        vd.days_from_eddi_to_first_art = self.days_from_eddi_to_first_art
        vd.days_from_eddi_to_current_art = self.days_from_eddi_to_current_art
        vd.region = self.subject.country.region_name
        vd.save()
        return vd

    def find_nearby_viral_load(self):
        earliest_date = self.visit_date - relativedelta(days=30)
        latest_date = self.visit_date + relativedelta(days=30)

        earlier_visit = Visit.objects.filter(
            viral_load__isnull=False,
            visit_date__range=[earliest_date, self.visit_date],
            on_treatment=self.on_treatment,
            subject=self.subject
        ).order_by('visit_date').exclude(pk=self.pk).last()

        later_visit = Visit.objects.filter(
            viral_load__isnull=False,
            visit_date__range=[self.visit_date, latest_date],
            on_treatment=self.on_treatment,
            subject=self.subject
        ).order_by('visit_date').exclude(pk=self.pk).first()

        if earlier_visit and later_visit:
            days_diff_later = (later_visit.visit_date - self.visit_date).days
            days_diff_earlier = (self.visit_date - earlier_visit.visit_date).days

            if days_diff_later < days_diff_earlier:
                update_visit(self, later_visit)
            else:
                update_visit(self, earlier_visit)
        elif earlier_visit:
            update_visit(self, earlier_visit)
        elif later_visit:
            update_visit(self, later_visit)


    def get_region(self):
        pass

    @property
    def ever_scope_ec(self):
        return Visit.objects.filter(subject=self.subject, scopevisit_ec=True).exists()
    

    @property
    def age_in_years(self):
        if not self.subject.date_of_birth:
            return None
        visit_date = self.visit_date
        born = self.subject.date_of_birth
        return visit_date.year - born.year - ((visit_date.month, visit_date.day) < (born.month, born.day))

    @property
    def is_after_aids_diagnosis(self):
        return bool(self.subject.aids_diagnosis_date and self.visit_date > self.subject.aids_diagnosis_date)

    @property
    def ever_aids_diagnosis(self):
        return bool(self.subject.aids_diagnosis_date)

    @property
    def days_since_cohort_entry(self):
        if self.subject.cohort_entry_date:
            return as_days(self.visit_date - self.subject.cohort_entry_date)

    @property
    def days_since_first_draw(self):
        earliest_visit_date = self.subject.earliest_visit_date
        if earliest_visit_date:
            return as_days(self.visit_date - self.subject.earliest_visit_date) or None
        
    @property
    def days_since_first_art(self):
        if not self.subject.art_initiation_date:
            return None
        if self.subject.art_initiation_date > self.visit_date:
            return None
        
        if self.subject.art_initiation_date is not None and self.on_treatment:
            return as_days(self.visit_date - self.subject.art_initiation_date)
        return None

    @property
    def days_since_current_art(self):
        if not self.on_treatment:
            return None

        if self.subject.art_resumption_date and self.subject.art_resumption_date < self.visit_date:
            return as_days(self.visit_date - self.subject.art_resumption_date)

        if self.subject.art_initiation_date:
            return as_days(self.visit_date - self.subject.art_initiation_date)

        return None

    @property
    def days_from_eddi_to_first_art(self):
        if self.subject.subject_eddi and self.subject.subject_eddi.eddi and self.subject.art_initiation_date:
            return as_days(self.subject.art_initiation_date - self.subject.subject_eddi.eddi)
        return None


    @property
    def days_from_eddi_to_current_art(self):
        if not self.on_treatment:
            return None

        if not (self.subject.subject_eddi and self.subject.subject_eddi.eddi):
            return None

        if self.subject.art_resumption_date and self.subject.art_resumption_date < self.visit_date:
            return as_days(self.subject.art_resumption_date - self.subject.subject_eddi.eddi)

        if self.subject.art_initiation_date:
            return as_days(self.subject.art_initiation_date - self.subject.subject_eddi.eddi)

        return None
    

class VisitDetail(models.Model):
    visit = OneToOneOrNoneField('Visit', related_name='visitdetail')

    is_after_aids_diagnosis = models.NullBooleanField()
    age_in_years = models.PositiveIntegerField(null=True)
    ever_aids_diagnosis = models.NullBooleanField()
    ever_scope_ec = models.NullBooleanField()
    earliest_visit_date = models.DateField(null=True)
    
    days_since_cohort_entry = models.IntegerField(null=True)
    days_since_first_draw = models.IntegerField(null=True)
    days_since_first_art = models.IntegerField(null=True)
    days_since_current_art = models.IntegerField(null=True)
    days_from_eddi_to_first_art = models.IntegerField(null=True)
    days_from_eddi_to_current_art = models.IntegerField(null=True)
    
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


class SpecimenQuerySet(QuerySet):
    def partial_matches(self, label, specimen_type):
        partial_label = label[0:4] # max 4 chars
        partial_label = u''.join(d for d in partial_label if d.isdigit())
        partial_label = partial_label.zfill(4)
        specimen_allowed_length = 7

        partial_matches = self.annotate(specimen_label_len=Length('specimen_label'))
        partial_matches = partial_matches.annotate(label_splitting_character=Lower(Substr('specimen_label', 5, 1)))
        partial_matches = partial_matches.filter(
            label_splitting_character="-",
            specimen_label_len=specimen_allowed_length,
            specimen_label__startswith=partial_label,
            specimen_type=specimen_type,
            parent_label__isnull=False
        )

        return partial_matches

class Specimen(models.Model):
    objects = SpecimenQuerySet.as_manager()
    
    VISIT_LINKAGE_CHOICES = (
        ('provisional','Provisional'),
        ('confirmed','Confirmed'),
        ('artificial','Artificial'),
    )
    ARTIFICIAL_LABEL_FORMAT = u'{specimen_label}-{specimen_index}-AA'

    class Meta:
        db_table = "cephia_specimens"

    specimen_label = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    parent_label = models.CharField(max_length=255, null=True, blank=True)
    subject_label = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    number_of_containers = models.IntegerField(null=True, blank=True)
    reported_draw_date = models.DateField(null=True, blank=True)
    transfer_in_date = models.DateField(null=True, blank=True)
    transfer_out_date = models.DateField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True)
    modified_date = models.DateField(null=True, blank=True)
    transfer_reason = models.CharField(max_length=50, null=True, blank=True)
    subject = ProtectedForeignKey(Subject, null=True, blank=False)
    visit = ProtectedForeignKey(Visit, null=True, blank=False, related_name='specimens')
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
    is_artificial = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.specimen_label

    def model_to_dict(self):
        d = model_to_dict(self)
        return d


    @classmethod
    def create_from_parent(cls, parent_specimen):
        inherited_fields = [
            'subject', 'subject_label', 'reported_draw_date', 
            'visit', 'visit_linkage', 'specimen_type',
            'volume_units', 'source_study'
        ]
        child_specimen = cls()
        for field in inherited_fields:
            setattr(child_specimen, field, getattr(parent_specimen, field))

        child_specimen.parent_label = parent_specimen.specimen_label
        child_specimen.parent = parent_specimen
        child_specimen.transfer_out_date = None #TODO: Add later
        child_specimen.shipped_to = None #TODO: Add later
        child_specimen.created_date = None
        child_specimen.aliquoting_reason = 'artificially_created'
        child_specimen.number_of_containers = 1
        child_specimen.artificial = True
        return child_specimen

    @classmethod
    def get_artificial_label(cls, label, **kwargs):
        index = 1
        specimen_label = cls.ARTIFICIAL_LABEL_FORMAT.format(specimen_label=label, specimen_index=unicode(index).zfill(2))

        while cls.objects.filter(specimen_label=specimen_label, **kwargs).first():
            index += 1
            specimen_label = cls.ARTIFICIAL_LABEL_FORMAT.format(specimen_label=label, specimen_index=unicode(index).zfill(2))
        return specimen_label

    @classmethod
    def update_or_create_specimen_for_label(cls, label, specimen_type, specimen_label_type=None, **kwargs):
        if specimen_label_type == 'aliquot_label' or specimen_label_type is None:
            return cls.objects.get(specimen_label=label, **kwargs)
        elif specimen_label_type == 'root_specimen':
            parent_specimen = cls.objects.get(specimen_label=label, parent__isnull=True, specimen_type=specimen_type, **kwargs)

            child_specimen = cls.create_from_parent(parent_specimen)
            child_specimen.specimen_label = cls.get_artificial_label(parent_specimen.specimen_label, **kwargs)
            return child_specimen
        
        elif specimen_label_type == 'aliquot_base':
            partial_match = cls.objects.partial_matches(label, specimen_type).first()

            if partial_match is None:
                raise cls.DoesNotExist('Could not find a partial match')
            child_specimen = cls.create_from_parent(partial_match.parent)
            child_specimen.specimen_label = cls.get_artificial_label(label, **kwargs)
            return child_specimen
            
        

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


class ViralLoadRow(ImportedRow):
    specimen_label = models.CharField(null=True, max_length=255)
    relation = models.CharField(null=True, max_length=255)
    value = models.CharField(null=True, max_length=255)
    comment = models.CharField(null=True, max_length=255)
    
    visit = ProtectedForeignKey(Visit, null=True)

class TreatmentStatusUpdateRow(ImportedRow):

    class Meta:
        db_table = "cephia_treatmentstatusupdate_rows"

    subject_label = models.CharField(max_length=255, null=False, blank=True)
    source_study = models.CharField(max_length=255, null=False, blank=True)
    
    art_initiation_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    art_initiation_date_mm = models.CharField(max_length=255, null=False, blank=True)
    art_initiation_date_dd = models.CharField(max_length=255, null=False, blank=True)
    art_interruption_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    art_interruption_date_mm = models.CharField(max_length=255, null=False, blank=True)
    art_interruption_date_dd = models.CharField(max_length=255, null=False, blank=True)
    art_resumption_date_yyyy = models.CharField(max_length=255, null=False, blank=True)
    art_resumption_date_mm = models.CharField(max_length=255, null=False, blank=True)
    art_resumption_date_dd = models.CharField(max_length=255, null=False, blank=True)

    subject = ProtectedForeignKey(Subject, null=True, blank=False)

    def __unicode__(self):
        return self.subject_label


def update_visit(current_visit, nearby_visit):
    viral_load_offset = (nearby_visit.visit_date - current_visit.visit_date).days
    current_visit.viral_load = nearby_visit.viral_load
    current_visit.vl_type = nearby_visit.vl_type
    current_visit.vl_detectable = nearby_visit.vl_detectable
    current_visit.viral_load_offset = viral_load_offset
    current_visit.save()



