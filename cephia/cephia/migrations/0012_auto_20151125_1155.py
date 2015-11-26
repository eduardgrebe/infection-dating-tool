# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0011_auto_20151102_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'assay', b'Assay')]),
        ),
        migrations.AlterField(
            model_name='historicalfileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'assay', b'Assay')]),
        ),
    ]
