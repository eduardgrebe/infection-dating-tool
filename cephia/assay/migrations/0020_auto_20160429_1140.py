# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0019_auto_20160428_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lsvitrosdiluentresult',
            name='final_SCO',
        ),
        migrations.RemoveField(
            model_name='lsvitrosdiluentresultrow',
            name='final_SCO',
        ),
        migrations.RemoveField(
            model_name='lsvitrosplasmaresult',
            name='final_SCO',
        ),
        migrations.RemoveField(
            model_name='lsvitrosplasmaresultrow',
            name='final_SCO',
        ),
        migrations.AlterField(
            model_name='lsvitrosdiluentresult',
            name='well',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
