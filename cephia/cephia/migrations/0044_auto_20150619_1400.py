# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0043_specimen_visit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specimen',
            name='child_label',
        ),
        migrations.AddField(
            model_name='specimen',
            name='specimen_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
