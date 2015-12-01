# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0013_auto_20151125_1212'),
        ('assay', '0003_panel_panelmemberships_panelshipment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PanelMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('replicates', models.IntegerField(null=True, blank=True)),
                ('panel', models.ForeignKey(to='assay.Panel', null=True)),
                ('visit', models.ForeignKey(to='cephia.Visit', null=True)),
            ],
            options={
                'db_table': 'cephia_panel_membership',
            },
        ),
        migrations.RemoveField(
            model_name='panelmemberships',
            name='panel',
        ),
        migrations.RemoveField(
            model_name='panelmemberships',
            name='visit',
        ),
        migrations.DeleteModel(
            name='PanelMemberships',
        ),
    ]
