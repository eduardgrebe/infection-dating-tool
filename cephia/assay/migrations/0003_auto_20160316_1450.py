# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0002_auto_20160316_1428'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='lagsediaresultrow',
            table='lagsedia_row',
        ),
    ]
