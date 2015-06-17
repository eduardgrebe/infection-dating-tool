# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0029_auto_20150616_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='patient_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
