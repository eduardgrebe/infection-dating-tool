# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0069_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='data_file',
            field=models.FileField(upload_to=b'/home/jarryd/id/cephia/cephia/cephia/../../media'),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='file_type',
            field=models.CharField(max_length=20, choices=[(b'subject', b'Subject'), (b'visit', b'Visit'), (b'transfer_in', b'Transfer In'), (b'aliquot', b'Aliquot'), (b'transfer_out', b'Transfer Out')]),
        ),
    ]
