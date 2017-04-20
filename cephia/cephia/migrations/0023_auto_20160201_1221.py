# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0022_auto_20160129_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileinfo',
            name='data_file',
            field=models.FileField(upload_to=b'/home/jarryd/id/cephia/cephia/cephia/../../media'),
        ),
    ]
