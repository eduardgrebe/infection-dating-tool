# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0017_auto_20150610_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='visit_cd4',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
