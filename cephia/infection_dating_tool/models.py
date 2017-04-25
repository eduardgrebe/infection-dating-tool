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
        
        map_codes = list(self.test_history.all().values_list('test_code', flat=True).distinct())
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


# class IDTUser(BaseUser):
#     class Meta:
#         db_table = "idt_users"
#         permissions = [
#         ]
    
#     password_reset_token = models.CharField(max_length=200, blank=True, null=True, db_index=True)

#     def __unicode__(self):
#         return "%s" % (self.username)

#     @classmethod
#     def generate_password_reset_link(self, user):
#         """ create an password authentication token for this user """
#         token = str(uuid.uuid4()).replace("-","").replace("_","")
#         user.password_reset_token = token
#         user.save()

#     def send_registration_notification(self):
#         email_context = {}
#         email_context['user'] = self.username
#         email_context['link_home'] = settings.SITE_BASE_URL
#         email_context = update_email_context(email_context)

#         if not self.has_usable_password():
#             IDTUser.generate_password_reset_link(self)
#             email_context['link_home'] = u'%s%s' % (settings.BASE_URL,
#                                                     reverse('finalise_user_account',
#                                                     kwargs={'token': self.password_reset_token}))

#         queue_templated_email(request=None, context=email_context,
#                               subject_template="Welcome to the Cephia Infection Dating Tool",
#                               text_template='infection_dating_tool/emails/signup.txt',
#                               html_template='infection_dating_tool/emails/new_member.html',
#                               to_addresses=[self.email],
#                               bcc_addresses=settings.BCC_EMAILS or [],
#                               from_address=settings.FROM_EMAIL)
