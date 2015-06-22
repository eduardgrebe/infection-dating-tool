# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0051_auto_20150622_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specimen',
            name='site',
        ),
        migrations.AlterField(
            model_name='specimen',
            name='source_study',
            field=models.ForeignKey(blank=True, to='cephia.Site', null=True),
        ),
    ]
