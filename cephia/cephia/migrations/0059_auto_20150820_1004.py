# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0058_auto_20150814_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='description',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='data_file',
            field=models.FileField(upload_to=b'/home/akshar/id/cephia/cephia/cephia/../../media'),
        ),
        migrations.AlterField(
            model_name='fileinfo',
            name='state',
            field=models.CharField(default=b'pending', max_length=10, choices=[(b'pending', b'Pending'), (b'imported', b'Imported'), (b'validated', b'Validated'), (b'error', b'Error')]),
        ),
    ]
