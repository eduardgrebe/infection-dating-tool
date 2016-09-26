from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TestHistoryFile(models.Model):
    test_history_file = models.FileField(upload_to="outside_eddi_uploads")
