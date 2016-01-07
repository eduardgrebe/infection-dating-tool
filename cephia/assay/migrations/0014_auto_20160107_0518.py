# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0019_auto_20160103_2227'),
        ('assay', '0013_assayresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lagresult',
            name='location',
        ),
        migrations.AddField(
            model_name='lagresult',
            name='laboratory',
            field=models.ForeignKey(to='cephia.Laboratory', max_length=255, null=True),
        ),
    ]
