# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0057_auto_20150722_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='description',
            field=models.CharField(default='to_be_deleted', max_length=255),
            preserve_default=False,
        ),
    ]
