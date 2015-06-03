# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0003_auto_20150601_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'/home/jarryd/id/cephia/cephia/cephia/../../media')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=2, choices=[(b'PE', b'PENDING'), (b'IM', b'IMPORTED'), (b'ER', b'ERROR')])),
                ('message', models.TextField()),
            ],
            options={
                'db_table': 'cephia_fileinfo',
            },
        ),
    ]
