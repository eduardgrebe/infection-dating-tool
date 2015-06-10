# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0019_auto_20150610_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimentype',
            name='spec_group',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
