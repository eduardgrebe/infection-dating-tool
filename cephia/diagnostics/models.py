from django.db import models
from cephia.models import Subject, ImportedRow
from django.db import transaction
from simple_history.models import HistoricalRecords


class DiagnosticTest(models.Model):
    class Meta:
        db_table = "cephia_diagnostic_tests"

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    history = HistoricalRecords()


class ProtocolLookup(models.Model):
    class Meta:
        db_table = "cephia_protocol_lookup"

    history = HistoricalRecords()
    name = models.CharField(max_length=100, null=False, blank=False)
    protocol = models.CharField(max_length=100, null=False, blank=False)
    test = models.ForeignKey(DiagnosticTest, null=False, blank=False)


class TestPropertyEstimate(models.Model):
    class Meta:
        db_table = "cephia_test_property_estimates"
        
    TYPE_CHOICES = (
        ('published','Published'),
        ('cephia','CEPHIA'),
        ('analogue','Analogue'),
        ('placeholder','Placeholder'),
    )
    
    history = HistoricalRecords()
    test = models.ForeignKey(DiagnosticTest, null=False, blank=True)
    estimate_label = models.CharField(max_length=255, null=False, blank=True)
    estimate_type = models.CharField(max_length=255, null=False, blank=True)
    mean_diagnostic_delay_days = models.IntegerField(null=True, blank=False)
    diagnostic_delay_median = models.IntegerField(null=True, blank=False)
    foursigma_diagnostic_delay_days = models.IntegerField(null=True, blank=False)
    is_default = models.BooleanField(blank=False, default=False)
    time0_ref = models.CharField(max_length=255, null=False, blank=True)
    comment = models.CharField(max_length=255, null=False, blank=True)
    reference = models.CharField(max_length=255, null=False, blank=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            result = super(TestPropertyEstimate, self).save(*args, **kwargs)
            if self.is_default:
                exists = TestPropertyEstimate.objects.filter(test=self.test, is_default=True).exclude(pk=self.pk).exists()
                if exists:
                    msg = "Default test already exists for %s" % (self.test.name)
                    raise ValueError(msg)

        return result


class DiagnosticTestHistory(models.Model):
    class Meta:
        db_table = "cephia_diagnostic_test_history"

    history = HistoricalRecords()
    subject = models.ForeignKey(Subject, null=True, blank=False, related_name='test_history')
    test = models.ForeignKey(DiagnosticTest, null=True, blank=False)
    test_date = models.DateField(null=True, blank=False)
    adjusted_date = models.DateField(null=True, blank=False)
    test_result = models.CharField(max_length=15, null=True, blank=False)
    ignore = models.BooleanField(blank=False, default=False)

    def __unicode__(self):
        return u'%s - %s' % (self.test_date, self.test_result)
    

class DiagnosticTestHistoryRow(ImportedRow):
    class Meta:
        db_table = "cephia_diagnostic_test_history_row"

    subject = models.CharField(max_length=255, null=False, blank=True)
    test_date = models.CharField(max_length=255, null=False, blank=True)
    test_code = models.CharField(max_length=255, null=False, blank=True)
    test_result = models.CharField(max_length=255, null=False, blank=True)
    source = models.CharField(max_length=255, null=False, blank=True)
    protocol = models.CharField(max_length=255, null=False, blank=True)
    test_history = models.ForeignKey(DiagnosticTestHistory, null=True, blank=False)
