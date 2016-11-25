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
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q

class OutsideEddiDiagnosticTestHistory(models.Model):
    class Meta:
        db_table = "outside_eddi_diagnostic_test_history"

    history = HistoricalRecords()
    subject = ProtectedForeignKey('OutsideEddiSubject', null=True, blank=False, related_name='outside_eddi_test_history')
    data_file = ProtectedForeignKey('OutsideEddiFileInfo', null=False, blank=False, related_name='test_history')
    test_code = models.CharField(max_length=25, null=True, blank=True)
    # test = ProtectedForeignKey('OutsideEddiDiagnosticTest', null=True, blank=False)
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


class OutsideEddiTestPropertyEstimateQuerySet(QuerySet):
    def for_user(self, user):
        return self.filter(models.Q(user=user) | models.Q(user=None))

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
    objects = OutsideEddiTestPropertyEstimateQuerySet.as_manager()
    
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

    code = models.CharField(max_length=25)
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
        ('mapped','Mapped'),
        ('error','Error')
    )

    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)
    data_file = models.FileField(upload_to=settings.MEDIA_ROOT+"/outside_eddi_uploads", null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=15, null=False, blank=False, default='pending')
    message = models.TextField(blank=True)
    history = HistoricalRecords()
    task_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.data_file.name

    def filename(self):
        return os.path.basename(self.data_file.name)

    def get_extension(self):
        return self.filename().split('.')[-1]

    def create_mapping(self, user):
        test_names = list(OutsideEddiDiagnosticTest.objects.filter(
            Q(user=user) | Q(user=None)
        ).values_list('name', flat=True))
        
        map_codes = list(self.test_history.all().values_list('test_code', flat=True).distinct())
        file_maps = []

        for code in map_codes:
            if TestPropertyMapping.objects.filter(code=code, user=user).exists():
                mapping = TestPropertyMapping.objects.get(code=code, user=user)
            elif code in test_names:
                test = OutsideEddiDiagnosticTest.objects.get(name=code)
                test_property = test.get_default_property()
            
                mapping = TestPropertyMapping.objects.create(
                    code=str(code),
                    test=test,
                    test_property=test_property,
                    user=user
                )
            else:
                mapping = TestPropertyMapping.objects.create(
                    code=code,
                    user=user
                )
            file_maps.append(mapping)

        return file_maps

    
class OutsideEddiSubject(models.Model):
    
    subject_label = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True, related_name='subjects')
    history = HistoricalRecords()
    edsc_reported  = models.DateField(null=True, blank=True, default=None)

    ep_ddi = models.DateField(null=True, blank=True)
    lp_ddi = models.DateField(null=True, blank=True)
    interval_size = models.IntegerField(null=True, blank=True)
    edsc_days_difference = models.IntegerField(null=True, blank=True)
    eddi = models.DateField(null=True, blank=True)
    recalculate = models.BooleanField(default=False)

    def __unicode__(self):
        return self.subject_label

    class Meta:
        unique_together = ("subject_label", "user")

    def calculate_eddi(self, user, data_file, lp_ddi, ep_ddi):
        edsc_days_diff = None
        # try:
        #     lp_ddi = OutsideEddiDiagnosticTestHistoryxbeo.objects.filter(data_file=data_file, subject=self, test_result='Positive', ignore=False).earliest('adjusted_date').adjusted_date
        # except OutsideEddiDiagnosticTestHistory.DoesNotExist:
        #     lp_ddi = None

        # try:
        #     ep_ddi = OutsideEddiDiagnosticTestHistory.objects.filter(data_file=data_file, subject=self, test_result='Negative', ignore=False).latest('adjusted_date').adjusted_date
        # except OutsideEddiDiagnosticTestHistory.DoesNotExist:
        #     ep_ddi = None

        if ep_ddi is None or lp_ddi is None:
            eddi = None
            interval_size = None
        else:
            eddi = ep_ddi + timedelta(days=((lp_ddi - ep_ddi).days / 2))
            interval_size = abs((lp_ddi - ep_ddi).days)

        if self.edsc_reported and eddi:
            edsc_days_diff = timedelta(days=(eddi - self.edsc_reported).days).days

        self.ep_ddi=ep_ddi
        self.lp_ddi=lp_ddi
        self.interval_size=interval_size
        self.edsc_days_difference=edsc_days_diff
        self.eddi = eddi
        self.save()
