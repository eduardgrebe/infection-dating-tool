# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-26 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestHistoryFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_history_file', models.FileField(upload_to='outside_eddi_uploads')),
            ],
        ),
    ]
