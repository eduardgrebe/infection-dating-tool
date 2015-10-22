# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.DateTimeField(auto_now_add=True)),
                ('description', models.DateTimeField(auto_now_add=True)),
                ('query', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'cephia_reports',
            },
        ),
    ]
