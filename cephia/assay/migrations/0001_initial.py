# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
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
                'db_table': 'cephia_assays',
            },
        ),
    ]
