# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0002_auto_20151109_1233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='panelmembership',
            name='replicates',
        ),
        migrations.RemoveField(
            model_name='panelmembershiprow',
            name='replicates',
        ),
        migrations.RemoveField(
            model_name='panelshipment',
            name='replicates',
        ),
        migrations.RemoveField(
            model_name='panelshipmentrow',
            name='replicates',
        ),
    ]
