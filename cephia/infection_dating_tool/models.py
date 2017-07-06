from __future__ import unicode_literals
import os
from django.conf import settings
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
from user_management.models import BaseUser
from cephia.models import CephiaUser

class IDTDiagnosticTestHistory(models.Model):
    class Meta:
        db_table = "idt_diagnostic_test_history"

    subject = ProtectedForeignKey('IDTSubject', null=True, blank=False, related_name='idt_test_history')
    data_file = ProtectedForeignKey('IDTFileInfo', null=False, blank=False, related_name='test_history')
    test_code = models.CharField(max_length=255, null=True, blank=True)
    test_date = models.DateField(null=True, blank=False)
    adjusted_date = models.DateField(null=True, blank=False)
    test_result = models.CharField(max_length=15, null=True, blank=False)

    def __unicode__(self):
        return u'%s - %s' % (self.test_date, self.test_result)


class IDTDiagnosticTest(models.Model):
    class Meta:
        db_table = "idt_diagnostic_tests"
        unique_together = ('name', 'user')

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

    def __str__(self):
        return '%s' % (self.name)

    def get_default_property(self):
        default_property = self.properties.get(global_default=True)

        return default_property


class IDTTestPropertyEstimateQuerySet(QuerySet):
    def for_user(self, user):
        return self.filter(models.Q(user=user) | models.Q(user=None))

class IDTTestPropertyEstimate(models.Model):
    class Meta:
        db_table = "idt_test_property_estimates"
        
    objects = IDTTestPropertyEstimateQuerySet.as_manager()
    
    user_default = models.BooleanField(blank=False, default=False)
    global_default = models.BooleanField(blank=False, default=False)
    test = models.ForeignKey(IDTDiagnosticTest, null=False, blank=True, related_name='properties')
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)

    estimate_label = models.CharField(max_length=255, null=False, blank=False)
    comment = models.CharField(max_length=255, null=False, blank=True)

    diagnostic_delay = models.FloatField(null=True, blank=True)
    diagnostic_delay_sigma = models.FloatField(null=True, blank=True)
    detection_threshold = models.FloatField(null=True, blank=True)
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

    def __str__(self):
        return '%s' % (self.id)


class TestPropertyMapping(models.Model):
    class Meta:
        db_table = "idt_test_property_mapping"
        unique_together = ('code', 'user')

    code = models.CharField(max_length=255)
    test = ProtectedForeignKey('IDTDiagnosticTest', null=True, blank=True)
    test_property = ProtectedForeignKey('IDTTestPropertyEstimate', null=True, blank=True)
    user = ProtectedForeignKey('cephia.CephiaUser')
    

class IDTFileInfo(models.Model):
    class Meta:
        db_table = "idt_file_info"

    STATE_CHOICES = (
        ('pending','Pending'),
        ('imported','Imported'),
        ('validated','Validated'),
        ('needs_mapping','Needs Mapping'),
        ('mapped','Mapped'),
        ('error','Error')
    )

    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)
    data_file = models.FileField(upload_to=settings.MEDIA_ROOT+"/infection_dating_tool_uploads", null=False, blank=False)
    file_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=15, null=False, blank=False, default='pending')
    message = models.TextField(blank=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.data_file.name

    def filename(self):
        return os.path.basename(self.data_file.name)

    def get_extension(self):
        return self.filename().split('.')[-1]

    def create_mapping(self, user):
        test_names = list(IDTDiagnosticTest.objects.filter(
            Q(user=user) | Q(user=None)
        ).values_list('name', flat=True))
        
        # map_codes = list(self.test_history.all().values_list('test_code', flat=True).distinct())
        map_codes = []
        for x in self.test_history.all().values_list('test_code', flat=True):
            if x not in map_codes:
                map_codes.append(x)
        file_maps = []

        for code in map_codes:
            if TestPropertyMapping.objects.filter(code=code, user=user).exists():
                mapping = TestPropertyMapping.objects.get(code=code, user=user)
            elif code in test_names:
                test = IDTDiagnosticTest.objects.get(name=code)
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

    
class IDTSubject(models.Model):
    class Meta:
        db_table = "idt_subjects"
        unique_together = ("subject_label", "user")
    
    subject_label = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True, related_name='subjects')
    edsc_reported  = models.DateField(null=True, blank=True, default=None)

    ep_ddi = models.DateField(null=True, blank=True)
    lp_ddi = models.DateField(null=True, blank=True)
    interval_size = models.IntegerField(null=True, blank=True)
    edsc_days_difference = models.IntegerField(null=True, blank=True)
    eddi = models.DateField(null=True, blank=True)
    flag = models.CharField(max_length=255, null=True, blank=False)

    def __unicode__(self):
        return self.subject_label

    def check_for_identical_dates(self, data_file):
        dates = data_file.test_history.filter(subject=self).values_list('test_date', flat=True)
        if len(set(dates)) == 1:
            return 'All tests reported are on same date\n'
        else:
            return ''

    def check_for_discordant_dates(self, data_file):
        pos_dates = data_file.test_history.filter(subject=self, test_result='Positive').values_list('test_date', flat=True).distinct()
        neg_dates = data_file.test_history.filter(subject=self, test_result='Negative').values_list('test_date', flat=True).distinct()
        duplicates = set(pos_dates).intersection(neg_dates)

        if duplicates:
            return 'Subject has a discordant test date\n'
        else:
            return ''

    def calculate_eddi(self, user, data_file, lp_ddi, ep_ddi):
        edsc_days_diff = None
        flag = self.check_for_identical_dates(data_file)
        
        if ep_ddi is None or lp_ddi is None:
            eddi = None
            interval_size = None
            if not lp_ddi:
                flag += 'Only negative tests reported\n'
            if not ep_ddi:
                flag += 'Only positive tests reported\n'
        else:
            flag += self.check_for_discordant_dates(data_file)
            eddi = ep_ddi + timedelta(days=((lp_ddi - ep_ddi).days / 2))
            interval_size = (lp_ddi - ep_ddi).days
            absolute_interval_size = abs(interval_size)

            if interval_size < 0:
                flag += 'Unexpected ordering of EPDDI and LPDDI\n'
            if absolute_interval_size < 10:
                flag += 'EPDDI and LPDDI less than 10 days apart\n'


        if flag:
            self.flag = flag

        if self.edsc_reported and eddi:
            edsc_days_diff = timedelta(days=(eddi - self.edsc_reported).days).days

        self.ep_ddi=ep_ddi
        self.lp_ddi=lp_ddi
        self.interval_size=interval_size
        self.edsc_days_difference=edsc_days_diff
        self.eddi = eddi
        self.save()


class IDTAllowedRegistrationEmails(models.Model):
    class Meta:
        db_table = "idt_allowed_registration_emails"

    email = models.CharField(max_length=200, blank=True, null=True, unique=True)


class SelectedCategory(models.Model):
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
    
    user = ProtectedForeignKey('cephia.CephiaUser', null=False)
    test = models.ForeignKey(IDTDiagnosticTest, null=True)
    category = models.CharField(choices=CATEGORIES, max_length=255, null=True)

    class Meta:
        unique_together = ('user', 'test')


class SelectedTest(models.Model):
    user = ProtectedForeignKey('cephia.CephiaUser', null=False)
    test = models.ForeignKey(IDTDiagnosticTest, null=False)

    class Meta:
        unique_together = ('user', 'test')


class GrowthRateEstimate(models.Model):
    growth_rate = models.FloatField(null=False, blank=False)
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)

    class Meta:
        unique_together = ('user', 'growth_rate')


class InfectiousPeriod(models.Model):
    class Meta:
        db_table = "idt_infectious_period"

    user = OneToOneOrNoneField('cephia.CephiaUser', null=True, blank=True)
    infectious_period = models.FloatField(null=False)
    infectious_period_input = models.FloatField(null=True, blank=False, verbose_name='Start of infectious period')
    viral_growth_rate = models.FloatField(null=True, blank=False)
    origin_viral_load = models.FloatField(null=True, blank=False, verbose_name='Viral load at origin/zero')
    viral_load = models.FloatField(null=True, blank=False, verbose_name='Viral load at start of infectious period')

    graph_file = models.FileField(upload_to="graphs", max_length=255, null=True)


class VariabilityAdjustment(models.Model):
    adjustment_factor = models.FloatField(null=False, blank=False, default=1.0, verbose_name='Intersubject variability adjustment factor (SDs)')
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True)

    class Meta:
        unique_together = ('user', 'adjustment_factor')
