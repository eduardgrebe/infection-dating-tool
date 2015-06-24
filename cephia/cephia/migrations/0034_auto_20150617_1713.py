# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0033_specimen_to_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimen',
            name='initial_claimed_volume',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='specimen',
            name='volume',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
