from __future__ import unicode_literals
import os
from django.conf import settings
from cephia.models import Subject
from simple_history.models import HistoricalRecords
from diagnostics.models import DiagnosticTest
from django.db import models

# Create your models here.
class TestHistoryFile(models.Model):

    STATE_CHOICES = (
        ('pending','Pending'),
        ('imported','Imported'),
        ('validated','Validated'),
        ('error','Error')
    )
    
    data_file = models.FileField(upload_to=settings.MEDIA_ROOT + "/outside_eddi_uploads")
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
