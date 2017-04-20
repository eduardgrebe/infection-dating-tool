# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0019_auto_20160128_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjecteddistatus',
            name='comment',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
