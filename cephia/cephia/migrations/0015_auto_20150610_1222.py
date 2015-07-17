# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0014_auto_20150610_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferinrow',
            name='draw_date',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='num_containers',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='patient_label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='sites',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='spec_type',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='specimen_label',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='transfer_reason',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='volume',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]