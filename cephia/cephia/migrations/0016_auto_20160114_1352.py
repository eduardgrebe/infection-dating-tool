# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0015_auto_20160114_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'', b'---------'), (b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'diagnostic_test', b'Diagnostic Test'), (b'protocol_lookup', b'Protocol Lookup'), (b'test_history', b'Diagnostic Test History'), (b'test_property', b'Diagnostic Test Properties')]),
        ),
        migrations.AlterField(
            model_name='historicalfileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'', b'---------'), (b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out'), (b'diagnostic_test', b'Diagnostic Test'), (b'protocol_lookup', b'Protocol Lookup'), (b'test_history', b'Diagnostic Test History'), (b'test_property', b'Diagnostic Test Properties')]),
        ),
    ]
