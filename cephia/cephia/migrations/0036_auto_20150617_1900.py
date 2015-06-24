# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0035_auto_20150617_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specimen',
            name='other_ref',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
