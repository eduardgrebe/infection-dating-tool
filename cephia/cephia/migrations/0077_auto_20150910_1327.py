# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0076_auto_20150910_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalspecimen',
            name='provisional_visit',
        ),
        migrations.RemoveField(
            model_name='specimen',
            name='provisional_visit',
        ),
        migrations.AddField(
            model_name='historicalspecimen',
            name='visit_linkage',
            field=models.CharField(max_length=12, null=True, choices=[(b'provisional', b'Provisional'), (b'confirmed', b'Confirmed'), (b'artificial', b'Artificial')]),
        ),
        migrations.AddField(
            model_name='specimen',
            name='visit_linkage',
            field=models.CharField(max_length=12, null=True, choices=[(b'provisional', b'Provisional'), (b'confirmed', b'Confirmed'), (b'artificial', b'Artificial')]),
        ),
    ]
