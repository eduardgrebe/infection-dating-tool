from __future__ import unicode_literals
import os
from django.conf import settings
from cephia.models import CephiaUser
from simple_history.models import HistoricalRecords
from django.db import models
from lib.fields import ProtectedForeignKey, OneToOneOrNoneField
from django.db import transaction
from django.db.models import QuerySet
from django.forms.models import model_to_dict
import collections
from world_regions import models as wr_models
from django.db.models.functions import Length, Substr, Lower
from django.contrib.auth.models import Group

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


class OutsideEddiDiagnosticTestHistory(models.Model):
    class Meta:
        db_table = "outside_eddi_diagnostic_test_history"

    history = HistoricalRecords()
    subject = ProtectedForeignKey('OutsideEddiSubject', null=True, blank=False, related_name='outside_eddi_test_history')
    test = ProtectedForeignKey('OutsideEddiDiagnosticTest', null=True, blank=False)
    test_date = models.DateField(null=True, blank=False)
    adjusted_date = models.DateField(null=True, blank=False)
    test_result = models.CharField(max_length=15, null=True, blank=False)
    ignore = models.BooleanField(blank=False, default=False)

    def __unicode__(self):
        return u'%s - %s' % (self.test_date, self.test_result)

class Study(models.Model):
    class Meta:
        unique_together = ("name", "user")

    name = models.CharField(max_length=50)
    user = ProtectedForeignKey('cephia.CephiaUser')

class OutsideEddiDiagnosticTest(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)
    description = models.CharField(max_length=255, null=False, blank=False)
    history = HistoricalRecords()

    class Meta:
        db_table = "outside_eddi_diagnostic_tests"
        unique_together = ('name', 'user')

    def __str__(self):
        return '%s' % (self.name)

    def get_default_property(self):
        default_property = self.properties.get(is_default=True)

        return default_property

class OutsideEddiProtocolLookup(models.Model):
    class Meta:
        db_table = "outside_eddi_cephia_protocol_lookup"

    history = HistoricalRecords()
    name = models.CharField(max_length=100, null=False, blank=False)
    protocol = models.CharField(max_length=100, null=False, blank=False)
    test = models.ForeignKey(OutsideEddiDiagnosticTest, null=False, blank=False)

class OutsideEddiTestPropertyEstimate(models.Model):
    class Meta:
        db_table = "outside_eddi_test_property_estimates"
        
    TYPE_CHOICES = (
        ('published','Published'),
        ('cephia','CEPHIA'),
        ('analogue','Analogue'),
        ('placeholder','Placeholder'),
        ('user_added','UserAdded'),
    )
    
    active_property = models.BooleanField(blank=False, default=False)
    estimate_label = models.CharField(max_length=255, null=False, blank=True)
    estimate_type = models.CharField(max_length=255, null=False, blank=True)
    
    history = HistoricalRecords()
    test = models.ForeignKey(OutsideEddiDiagnosticTest, null=False, blank=True, related_name='properties')
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)
    
    mean_diagnostic_delay_days = models.IntegerField(null=True, blank=False)
    diagnostic_delay_median = models.IntegerField(null=True, blank=True)
    foursigma_diagnostic_delay_days = models.IntegerField(null=True, blank=True)
    is_default = models.BooleanField(blank=False, default=False)
    time0_ref = models.CharField(max_length=255, null=False, blank=True)
    comment = models.CharField(max_length=255, null=False, blank=True)
    reference = models.CharField(max_length=255, null=False, blank=True)

    def __str__(self):
        return '%s' % (self.id)


class TestPropertyMapping(models.Model):

    code = models.CharField(max_length=10)
    test = ProtectedForeignKey('OutsideEddiDiagnosticTest', null=True, blank=True)
    test_property = ProtectedForeignKey('OutsideEddiTestPropertyEstimate', null=True, blank=True)
    user = ProtectedForeignKey('cephia.CephiaUser')

    class Meta:
        unique_together = ('code', 'user')


class OutsideEddiFileInfo(models.Model):

    STATE_CHOICES = (
        ('pending','Pending'),
        ('imported','Imported'),
        ('validated','Validated'),
        ('needs_mapping','Needs Mapping'),
        ('error','Error')
    )

    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)
    data_file = models.FileField(upload_to=settings.MEDIA_ROOT+"/outside_eddi_uploads", null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=15, null=False, blank=False, default='pending')
    message = models.TextField(blank=True)
    history = HistoricalRecords()
    task_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __unicode__(self):
        return self.data_file.name

    def filename(self):
        return os.path.basename(self.data_file.name)

    def get_extension(self):
        return self.filename().split('.')[-1]


class OutsideEddiSubject(models.Model):
    
    subject_label = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    test_date = models.DateField(null=True, blank=True)
    test_code = models.CharField(max_length=25, null=True, blank=True)
    test_result = models.CharField(max_length=8, null=True, blank=True)

    data_file = ProtectedForeignKey('OutsideEddiFileInfo', null=False, blank=False, related_name='subjects')
    
    ep_ddi = models.DateField(null=True, blank=True)
    lp_ddi = models.DateField(null=True, blank=True)
    interval_size = models.IntegerField(null=True, blank=True)
    edsc_days_difference = models.IntegerField(null=True, blank=True)
    eddi = models.DateField(null=True, blank=True)
    recalculate = models.BooleanField(default=False)
    eddi_type = models.CharField(max_length=100, null=False, blank=False)
    history = HistoricalRecords()

    def __unicode__(self):
        return self.subject_label
