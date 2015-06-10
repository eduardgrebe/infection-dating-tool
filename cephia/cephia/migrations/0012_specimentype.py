# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0011_auto_20150609_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecimenType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('spec_type', models.IntegerField()),
                ('spec_group', models.IntegerField()),
            ],
            options={
                'db_table': 'cephia_specimen_type',
            },
        ),
    ]
