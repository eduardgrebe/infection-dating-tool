from __future__ import unicode_literals
import os
from django.conf import settings
from cephia.models import Subject, CephiaUser, ImportedRow
from simple_history.models import HistoricalRecords
from diagnostics.models import DiagnosticTest
from django.db import models
from lib.fields import ProtectedForeignKey, OneToOneOrNoneField
from django.db import transaction

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

class TestHistoryFile(models.Model):

    STATE_CHOICES = (
        ('pending','Pending'),
        ('imported','Imported'),
        ('validated','Validated'),
        ('error','Error')
    )
    
    data_file = models.FileField(upload_to="uploads/outside_eddi_uploads")
    state = models.CharField(choices=STATE_CHOICES, max_length=10, null=False, blank=False, default='pending')

    def filename(self):
        return 'outside_eddi_uploads/' + os.path.basename(self.data_file.name)

    def get_extension(self):
        return self.filename().split('.')[-1]

class OutsideEddiDiagnosticTestHistory(models.Model):
    class Meta:
        db_table = "outside_eddi_diagnostic_test_history"

    history = HistoricalRecords()
    subject = models.ForeignKey(Subject, null=True, blank=False, related_name='outside_eddi_test_history')
    test = models.ForeignKey(DiagnosticTest, null=True, blank=False)
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

class OutsideEddiDiagnosticTestHistoryRow(ImportedRow):
    class Meta:
        db_table = "outside_eddi_cephia_diagnostic_test_history_row"

    subject = models.CharField(max_length=255, null=False, blank=True)
    test_date = models.CharField(max_length=255, null=False, blank=True)
    test_code = models.CharField(max_length=255, null=False, blank=True)
    test_result = models.CharField(max_length=255, null=False, blank=True)
    source = models.CharField(max_length=255, null=False, blank=True)
    protocol = models.CharField(max_length=255, null=False, blank=True)
    test_history = models.ForeignKey(OutsideEddiDiagnosticTestHistory, null=True, blank=False)

class TestPropertyMapping(models.Model):

    code = models.CharField(max_length=10)
    test = ProtectedForeignKey('OutsideEddiDiagnosticTest', null=True, blank=True)
    test_property = ProtectedForeignKey('OutsideEddiTestPropertyEstimate', null=True, blank=True)
    user = ProtectedForeignKey('cephia.CephiaUser')

    class Meta:
        unique_together = ('code', 'user')

class EDDITable(models.Model):
    user = ProtectedForeignKey('cephia.CephiaUser')
    test_file = ProtectedForeignKey('TestHistoryFile')
    subject = models.CharField(max_length=255, null=False, blank=False)
    dates = models.DateField(null=True, blank=False)
    results = models.CharField(max_length=15, null=True, blank=False)

# class OutsideEddiFileInfo(models.Model):

#     class Meta:
#         db_table = "outside_eddi_datafiles"

#     STATE_CHOICES = (
#         ('pending','Pending'),
#         ('imported','Imported'),
#         ('validated','Validated'),
#         ('error','Error')
#     )

#     SPECIMEN_LABEL_TYPES = [
#         ('aliquot_label', 'Aliquot Label'),
#         ('root_specimen', 'Root Specimen'),
#         ('aliquot_base', 'Aliquot Base'),
#     ]

#     data_file = models.FileField(upload_to=settings.MEDIA_ROOT, null=False, blank=False)
#     file_type = models.CharField(max_length=50, null=False, blank=False, choices=FILE_TYPE_CHOICES)
#     # assay = ProtectedForeignKey(OutsideEddiAssay, db_index=True, default=None, null=True)
#     # panel = ProtectedForeignKey(OutsideEddiPanel, db_index=True, default=None, null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     state = models.CharField(choices=STATE_CHOICES, max_length=10, null=False, blank=False, default='pending')
#     priority = models.IntegerField(null=False, blank=False, default=1)
#     message = models.TextField(blank=True)
#     history = HistoricalRecords()
#     task_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
#     specimen_label_type = models.CharField(max_length=255, choices=SPECIMEN_LABEL_TYPES, blank=True, default='aliquot_label')

#     def __unicode__(self):
#         return self.data_file.name

#     def filename(self):
#         return os.path.basename(self.data_file.name)

#     def get_handler(self):
#         if self.assay:
#             return get_file_handler_for_type(self.file_type, self.assay.name)(self)
#         else:
#             return get_file_handler_for_type(self.file_type, None)(self)

#     def get_row(self, row_id):
#         if self.file_type == 'subject':
#             return SubjectRow.objects.get(fileinfo__id=self.id, id=row_id)
#         elif self.file_type == 'visit':
#             return VisitRow.objects.get(fileinfo__id=self.id, id=row_id)
#         elif self.file_type == 'transfer_in':
#             return TransferInRow.objects.get(fileinfo__id=self.id, id=row_id)
#         elif self.file_type == 'aliquot':
#             return AliquotRow.objects.get(fileinfo__id=self.id, id=row_id)
#         elif self.file_type == 'transfer_out':
#             return TransferOutRow.objects.get(fileinfo__id=self.id, id=row_id)
#         elif self.file_type == 'panel_membership':
#             return PanelMembershipRow.objects.get(fileinfo__id=self.id, id=row_id)
#         elif self.file_type == 'panel_shipment':
#             return PanelShipmentRow.objects.get(fileinfo__id=self.id, id=row_id)
#         if self.file_type == 'viral_load':
#             return ViralLoadRow.objects.get(fileinfo__id=self.id, id=row_id)
#         elif self.file_type == 'assay':
#             if self.assay.name == 'lag':
#                 return LagResultRow.objects.get(fileinfo__id=self.id, id=row_id)
#             elif self.assay.name == 'biorad':
#                 return BioradResultRow.objects.get(fileinfo__id=self.id, id=row_id)

#     def get_extension(self):
#         return self.filename().split('.')[-1]

# class OutsideEddiAssay(models.Model):
#     class Meta:
#         db_table = "outside_eddi_assay"

#     name = models.CharField(max_length=255, null=False, blank=False)
#     long_name = models.CharField(max_length=255, null=False, blank=False)
#     developer = models.CharField(max_length=255, null=False, blank=False)
#     description = models.CharField(max_length=255, null=False, blank=False)

#     def __unicode__(self):
#         return "%s" % (self.name)

# class OutsideEddiPanel(models.Model):

#     class Meta:
#         db_table = "outside_eddi_panels"

#     short_name = models.CharField(max_length=50, null=True, blank=True)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     description = models.TextField(null=True, blank=False)
#     # specimen_type = ProtectedForeignKey(OutsideEddiSpecimenType, null=True, blank=False, db_index=True)
#     volume = models.FloatField(null=True, blank=True)
#     n_recent = models.IntegerField(null=True, blank=False)
#     n_longstanding = models.IntegerField(null=True, blank=False)
#     n_challenge = models.IntegerField(null=True, blank=False)
#     n_reproducibility_controls = models.IntegerField(null=True, blank=False)
#     n_negative = models.IntegerField(null=True, blank=False)
#     n_total = models.IntegerField(null=True, blank=False)
#     blinded = models.NullBooleanField()
#     notes = models.TextField(null=True, blank=False)
#     visits = models.ManyToManyField('Visit', through='assay.PanelMembership', related_name='panels')

#     def __unicode__(self):
#         return self.short_name or self.name

# class OutsideEddiSpecimenType(models.Model):

#     class Meta:
#         db_table = "outside_eddi_specimen_types"

#     name = models.CharField(max_length=255, null=False, blank=False)
#     spec_type = models.CharField(max_length=10, null=False, blank=False)
#     spec_group = models.IntegerField(null=True, blank=True)

#     def __unicode__(self):
#         return self.name
