# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0015_auto_20151211_1014'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=255)),
                ('long_name', models.CharField(max_length=255)),
                ('developer', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cephia_assay',
            },
        ),
        migrations.AddField(
            model_name='fileinfo',
            name='assay',
            field=models.ForeignKey(default=None, to='cephia.Assay', null=True),
        ),
        migrations.AddField(
            model_name='historicalfileinfo',
            name='assay',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='cephia.Assay', null=True),
        ),
    ]
