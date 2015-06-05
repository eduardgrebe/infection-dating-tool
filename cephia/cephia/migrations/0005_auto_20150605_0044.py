# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0004_ethnicity_fileinfo_subject_subjectrow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subtype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'cephia_subtype',
            },
        ),
        migrations.AlterField(
            model_name='subject',
            name='gender',
            field=models.CharField(blank=True, max_length=6, choices=[(b'pending', b'Pending'), (b'processed', b'Processed'), (b'error', b'Error')]),
        ),
    ]
