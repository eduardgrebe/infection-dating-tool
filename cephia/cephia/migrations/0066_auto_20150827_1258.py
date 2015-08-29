# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0065_auto_20150827_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliquotrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', blank=True),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', blank=True),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', blank=True),
        ),
        migrations.AlterField(
            model_name='transferoutrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', blank=True),
        ),
        migrations.AlterField(
            model_name='visitrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', blank=True),
        ),
    ]
