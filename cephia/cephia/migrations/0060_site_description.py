# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0015_auto_20150825_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='description',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]
