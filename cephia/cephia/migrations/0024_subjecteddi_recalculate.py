# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0023_auto_20160201_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjecteddi',
            name='recalculate',
            field=models.BooleanField(default=False),
        ),
    ]
