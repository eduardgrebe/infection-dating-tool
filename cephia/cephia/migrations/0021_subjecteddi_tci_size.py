# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0020_auto_20160128_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjecteddi',
            name='tci_size',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
