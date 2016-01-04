# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0007_auto_20160101_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panelmembership',
            name='panel',
            field=models.ForeignKey(to='cephia.Panels', null=True),
        ),
        migrations.AlterField(
            model_name='panelshipment',
            name='panel',
            field=models.ForeignKey(to='cephia.Panels', null=True),
        ),
    ]
