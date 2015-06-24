# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0052_auto_20150622_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='visit_cd4',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='visit_vl',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
