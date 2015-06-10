# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0016_auto_20150610_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='visit_cd4',
            field=models.IntegerField(blank=True),
        ),
    ]
