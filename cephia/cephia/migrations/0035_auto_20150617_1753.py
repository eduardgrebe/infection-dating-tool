# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0034_auto_20150617_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimen',
            name='num_containers',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
