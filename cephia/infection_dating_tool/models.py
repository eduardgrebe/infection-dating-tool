from __future__ import unicode_literals
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models import QuerySet
import math
import os

from . import calculations
from lib.fields import ProtectedForeignKey, OneToOneOrNoneField


class IDTDiagnosticTestHistory(models.Model):
    class Meta:
        db_table = "idt_diagnostic_test_history"

    subject = ProtectedForeignKey('IDTSubject', null=True, blank=False, related_name='idt_test_history')
    data_file = ProtectedForeignKey('IDTFileInfo', null=False, blank=False, related_name='test_history')
    test_code = models.CharField(max_length=255, null=True, blank=True)
    test_date = models.DateField(null=True, blank=False)
    adjusted_date = models.DateField(null=True, blank=False)
    test_result = models.CharField(max_length=15, null=True, blank=False)
    diagnostic_delay = models.FloatField(null=True, blank=True)
    sigma = models.FloatField(null=True, blank=True)
    warning = models.CharField(max_length=255, null=True, blank=True)

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

    def get_diagnostic_delay_for_residual_risk(self, user):
        test_prop = self.properties.get(global_default=True)

        if not self.category == 'viral_load':
            diagnostic_delay = test_prop.diagnostic_delay
        else:
            growth_rate = get_user_growth_rate(user).growth_rate
            diagnostic_delay = math.log10(test_prop.detection_threshold) / growth_rate

        return diagnostic_delay


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
        ('pending', 'Pending'),
        ('imported', 'Imported'),
        ('validated', 'Validated'),
        ('needs_mapping', 'Needs Mapping'),
        ('mapped', 'Mapped'),
        ('error', 'Error')
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
    ep_ddi = models.DateField(null=True, blank=True)
    lp_ddi = models.DateField(null=True, blank=True)
    interval_size = models.IntegerField(null=True, blank=True)
    eddi = models.DateField(null=True, blank=True)
    flag = models.CharField(max_length=512, null=True, blank=False)

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

    def calculate_eddi(self, user, data_file, lp_ddi_dict, ep_ddi_dict):
        flag = self.check_for_identical_dates(data_file)

        ci, created = CredibilityInterval.objects.get_or_create(user=user)
        neg_adjusted_date = ep_ddi_dict.get('date')
        neg_sigma = ep_ddi_dict.get('sigma')
        neg_diagnostic_delay = ep_ddi_dict.get('diagnostic_delay')

        pos_adjusted_date = lp_ddi_dict.get('date')
        pos_sigma = lp_ddi_dict.get('sigma')
        pos_diagnostic_delay = lp_ddi_dict.get('diagnostic_delay')

        big_delta = None
        if pos_adjusted_date and neg_adjusted_date:
            big_delta = (pos_adjusted_date - neg_adjusted_date).days
        ep_ddi = None
        lp_ddi = None

        ci_failed = False
        calculate_ci = ci.calculate_ci
        if (big_delta and big_delta <= 0) and calculate_ci:
            calculate_ci = False
            flag += 'Credibility interval cannot be calculated if results are in unexpexted order\n'
        elif not big_delta and calculate_ci:
            calculate_ci = False
            flag += 'Credibility interval cannot be calculated without both negative and positive results\n'

        if not ep_ddi_dict or not lp_ddi_dict:
            eddi = None
            interval_size = None
            if not lp_ddi_dict:
                flag += 'Only negative tests reported\n'
            if not ep_ddi_dict:
                flag += 'Only positive tests reported\n'
            ep_ddi = ep_ddi_dict.get('date')
            lp_ddi = lp_ddi_dict.get('date')

        elif calculate_ci:
            t1 = 0
            d1 = neg_diagnostic_delay
            sigma1 = neg_sigma
            delta1, scale1, error = calculations.find_delta_scale(d1, sigma1)

            t2 = big_delta
            d2 = pos_diagnostic_delay
            sigma2 = pos_sigma
            delta2, scale2, error = calculations.find_delta_scale(d2, sigma2)

            if not error:
                alpha = ci.alpha
                ep_ddi_t, lp_ddi_t, error = calculations.find_ci_limits(
                    t1, t2, scale1, delta1, scale2, delta2, alpha
                )
                ep_ddi = ep_ddi_dict['date'] + relativedelta(days=ep_ddi_t)
                lp_ddi = ep_ddi_dict['date'] + relativedelta(days=lp_ddi_t)

            if error:
                ci_failed = True
                flag += error
            else:
                flag += 'EP-DDI & LP-DDI represent {}% Credibility Interval\n'.format(int(round((1 - alpha) * 100)))

        else:
            ep_ddi = ep_ddi_dict.get('date')
            lp_ddi = lp_ddi_dict.get('date')
            flag += 'EP-DDI & LP-DDI based on median diagnostic delays\n'

        if ci_failed:
            ep_ddi = ep_ddi_dict.get('date')
            lp_ddi = lp_ddi_dict.get('date')
            flag += 'Credibility interval could not be calculated. EP-DDI & LP-DDI based on median diagnostic delays\n'

        if ep_ddi and lp_ddi:
            flag += self.check_for_discordant_dates(data_file)
            interval_size = (lp_ddi - ep_ddi).days
            eddi = ep_ddi + timedelta(days=(interval_size / 2))

        absolute_interval_size = None
        if interval_size or interval_size == 0:
            absolute_interval_size = abs(interval_size)

        if (interval_size or interval_size == 0) and interval_size < 0:
            flag += 'Unexpected ordering of EPDDI and LPDDI\n'
        if (absolute_interval_size or absolute_interval_size == 0) and absolute_interval_size < 10:
            flag += 'EPDDI and LPDDI less than 10 days apart\n'

        if flag:
            self.flag = flag

        self.ep_ddi = ep_ddi
        self.lp_ddi = lp_ddi
        self.interval_size = interval_size
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


class ResidualRisk(models.Model):
    class Meta:
        db_table = "idt_residual_risk"

    CHOICES = (
        ('estimates', 'Estimates'),
        ('data', 'Data'),
        ('supply', 'Supply'),
    )

    choice = models.CharField(choices=CHOICES, max_length=255, null=False, default='estimates')

    user = OneToOneOrNoneField('cephia.CephiaUser', null=True, blank=True)
    residual_risk = models.FloatField(null=False, default=0)
    residual_risk_input = models.FloatField(null=False, default=0)

    infectious_period = models.FloatField(null=False)
    infectious_period_input = models.FloatField(
        null=False, blank=False, default=0, verbose_name='Start of infectious period')

    viral_growth_rate = models.FloatField(null=True, blank=False)
    origin_viral_load = models.FloatField(null=True, blank=False, verbose_name='Viral load at origin/zero')
    viral_load = models.FloatField(null=True, blank=False, verbose_name='Viral load at start of infectious period')

    confirmed_transmissions = models.IntegerField(null=True, blank=False)
    screening_test = ProtectedForeignKey('IDTDiagnosticTest', null=True, related_name='screening')
    positive_test = ProtectedForeignKey('IDTDiagnosticTest', null=True, related_name='positive')
    negative_test = ProtectedForeignKey('IDTDiagnosticTest', null=True, related_name='negative')

    ci_lower_bound = models.FloatField(null=True)
    ci_upper_bound = models.FloatField(null=True)

    graph_file_probability = models.FileField(upload_to="graphs", max_length=255, null=True)
    graph_file_donations = models.FileField(upload_to="graphs", max_length=255, null=True)
    upper_limit = models.FloatField(null=False, default=0)


class CredibilityInterval(models.Model):
    calculate_ci = models.BooleanField(blank=False, default=False)
    alpha = models.FloatField(null=False, blank=False, default=0.05, verbose_name='Significance level (alpha) for credibility intervals')
    user = ProtectedForeignKey('cephia.CephiaUser', null=True, blank=True, unique=True)


def get_user_growth_rate(user):
    growth_rate = GrowthRateEstimate.objects.filter(user=user).first()
    if not growth_rate:
        growth_rate = GrowthRateEstimate.objects.get(user__isnull=True)
        growth_rate.pk = None
        growth_rate.user = user
        growth_rate.save()

    return growth_rate
