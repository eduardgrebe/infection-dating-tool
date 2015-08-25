# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0010_auto_20150825_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='scopevisit_ec',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
