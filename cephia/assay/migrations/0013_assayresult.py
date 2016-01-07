# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0019_auto_20160103_2227'),
        ('assay', '0012_auto_20160106_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssayResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_date', models.DateField(null=True)),
                ('result', models.FloatField(null=True)),
                ('assay', models.ForeignKey(to='cephia.Assay', null=True)),
                ('panel', models.ForeignKey(to='cephia.Panels', null=True)),
                ('specimen', models.ForeignKey(to='cephia.Specimen', null=True)),
            ],
            options={
                'db_table': 'cephia_assay_results',
            },
        ),
    ]
