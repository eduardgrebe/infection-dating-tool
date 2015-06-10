# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0009_visit_visit_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectrow',
            name='state',
            field=models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')]),
        ),
        migrations.AlterField(
            model_name='visitrow',
            name='state',
            field=models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')]),
        ),
    ]
