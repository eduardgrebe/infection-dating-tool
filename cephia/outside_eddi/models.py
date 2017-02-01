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
    test_code = models.CharField(max_length=255, null=True, blank=True)
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
    CATEGORIES = (
        ('1st_gen_lab', '1st Gen Lab Assay (Viral Lysate IgG sensitive Antibody)'),
        ('2nd_gen_lab', '2nd Gen Lab Assay (Recombinant IgG sensitive Antibody)'),
        ('2nd_gen_rapid', '2nd Gen Rapid Test'),
        ('3rd_gen_lab', '3rd Gen Lab Assay (IgM sensitive Antibody)'),
        ('3rd_gen_rapid', '3rd Gen Rapid Test'),
        ('4th_gen_lab', '4th Gen Lab Assay (p24 Ag/Ab Combo)'),
        ('4th_gen_rapid', '4th Gen Rapid Test'),
        ('dpp', 'DPP'),
        ('immunofluorescence_assay', 'Immunofluorescence Assay'),
        ('p24_antigen', 'p24 Antigen'),
        ('viral_load', 'Viral Load'),
        ('western_blot', 'Western blot'),
    )
    
    name = models.CharField(max_length=255, null=False, blank=False)
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)
    category = models.CharField(choices=CATEGORIES, max_length=255, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "outside_eddi_diagnostic_tests"
        unique_together = ('name', 'user')

    def __str__(self):
        return '%s' % (self.name)

    def get_default_property(self):
        default_property = self.properties.get(is_default=True)

        return default_property


class OutsideEddiTestPropertyEstimateQuerySet(QuerySet):
    def for_user(self, user):
        return self.filter(models.Q(user=user) | models.Q(user=None))

class OutsideEddiTestPropertyEstimate(models.Model):
    class Meta:
        db_table = "outside_eddi_test_property_estimates"
        
    objects = OutsideEddiTestPropertyEstimateQuerySet.as_manager()
    
    active_property = models.BooleanField(blank=False, default=False)
    is_default = models.BooleanField(blank=False, default=False)
    test = models.ForeignKey(OutsideEddiDiagnosticTest, null=False, blank=True, related_name='properties')
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)

    estimate_label = models.CharField(max_length=255, null=False, blank=True)
    comment = models.CharField(max_length=255, null=False, blank=True)


    diagnostic_delay = models.FloatField(null=True, blank=False)
    diagnostic_delay_mean = models.FloatField(null=True, blank=False)
    diagnostic_delay_mean_se = models.FloatField(null=True, blank=False)
    diagnostic_delay_mean_ci_lower = models.FloatField(null=True, blank=False)
    diagnostic_delay_mean_ci_upper = models.FloatField(null=True, blank=False)

    diagnostic_delay_median = models.FloatField(null=True, blank=False)
    diagnostic_delay_median_se = models.FloatField(null=True, blank=False)
    diagnostic_delay_median_ci_lower = models.FloatField(null=True, blank=False)
    diagnostic_delay_median_ci_upper = models.FloatField(null=True, blank=False)
    diagnostic_delay_range = models.CharField(max_length=255, null=True, blank=True)
    diagnostic_delay_iqr = models.CharField(max_length=255, null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return '%s' % (self.id)


class TestPropertyMapping(models.Model):

    code = models.CharField(max_length=255)
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
    file_name = models.CharField(max_length=255)
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
