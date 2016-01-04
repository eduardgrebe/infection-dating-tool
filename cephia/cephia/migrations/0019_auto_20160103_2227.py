# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0018_auto_20160101_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='Panels',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('volume', models.FloatField(null=True, blank=True)),
                ('specimen_type', models.ForeignKey(to='cephia.SpecimenType', null=True)),
            ],
            options={
                'db_table': 'cephia_panel',
            },
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='panel',
            field=models.ForeignKey(default=None, to='cephia.Panels', null=True),
        ),
        migrations.AddField(
            model_name='historicalfileinfo',
            name='panel',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Panels', null=True),
        ),
    ]
