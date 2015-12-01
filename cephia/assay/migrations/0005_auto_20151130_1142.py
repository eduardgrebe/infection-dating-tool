# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0004_auto_20151130_1142'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='panelmembership',
            table='cephia_panel_memberships',
        ),
    ]
