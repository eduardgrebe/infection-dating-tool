from django.db import models
from cephia.models import Subject, ImportedRow


class DiagnosticTest(models.Model):
    class Meta:
        db_table = "diagnostic_tests"

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)


class ProtocolLookup(models.Model):
    class Meta:
        db_table = "protocol_lookup"

    name = models.CharField(max_length=100, null=False, blank=False)
    protocol = models.CharField(max_length=100, null=False, blank=False)
    test = models.ForeignKey(DiagnosticTest, null=False, blank=False)


class TestPropertyEstimate(models.Model):
    class Meta:
        db_table = "test_property_estimates"
        
    TYPE_CHOICES = (
        ('published','Published'),
        ('cephia','CEPHIA'),
        ('analogue','Analogue'),
        ('placeholder','Placeholder'),
    )
    
    test = models.ForeignKey(DiagnosticTest, null=False, blank=True)
    estimate_label = models.CharField(max_length=255, null=False, blank=True)
    estimate_type = models.CharField(max_length=255, null=False, blank=True)
    mean_diagnostic_delay_days = models.IntegerField(null=True, blank=False)
    foursigma_diagnostic_delay_days = models.IntegerField(null=True, blank=False)
    is_default = models.BooleanField(blank=False, default=False)
    comment = models.CharField(max_length=255, null=False, blank=True)
    reference = models.CharField(max_length=255, null=False, blank=True)


class DiagnosticTestHistoryRow(ImportedRow):
    class Meta:
        db_table = "diagnostic_test_history_row"

    subject = models.CharField(max_length=255, null=False, blank=True)
    test_date = models.CharField(max_length=255, null=False, blank=True)
    test_code = models.CharField(max_length=255, null=False, blank=True)
    test_result = models.CharField(max_length=255, null=False, blank=True)
    source = models.CharField(max_length=255, null=False, blank=True)
    protocol = models.CharField(max_length=255, null=False, blank=True)


class DiagnosticTestHistory(models.Model):
    class Meta:
        db_table = "diagnostic_test_history"

    subject = models.ForeignKey(Subject, null=True, blank=False)
    test = models.ForeignKey(DiagnosticTest, null=True, blank=False)
    test_date = models.DateField(null=True, blank=False)
    adjusted_date = models.DateField(null=True, blank=False)
    test_result = models.CharField(max_length=15, null=True, blank=False)
