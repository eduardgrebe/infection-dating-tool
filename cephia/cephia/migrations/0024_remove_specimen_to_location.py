# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0023_auto_20150610_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specimen',
            name='to_location',
        ),
    ]
