# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0036_auto_20150617_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimen',
            name='other_ref',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
