# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0040_auto_20150617_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='specimen',
            name='aliquoting_reason',
            field=models.ForeignKey(blank=True, to='cephia.AliquotingReason', null=True),
        ),
        migrations.AddField(
            model_name='specimen',
            name='panel_inclusion_criteria',
            field=models.ForeignKey(blank=True, to='cephia.PanelInclusionCriteria', null=True),
        ),
    ]
