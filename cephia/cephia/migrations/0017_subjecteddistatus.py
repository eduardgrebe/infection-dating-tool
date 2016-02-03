# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0016_auto_20160114_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectEDDIStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=20, null=True, choices=[(b'ok', b'OK'), (b'investigate', b'Investigate'), (b'other', b'Other')])),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'cephia_subject_eddi_status',
            },
        ),
    ]
