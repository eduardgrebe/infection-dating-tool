# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0038_auto_20150617_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specimen',
            name='annihilation_date',
        ),
    ]
