# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0021_subjecteddi_tci_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='data_file',
            field=models.FileField(upload_to=b'/home/gtp/id/cephia/src/cephia/cephia/../../media'),
        ),
    ]
