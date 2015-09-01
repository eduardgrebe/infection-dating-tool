# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0064_auto_20150827_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliquotrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AddField(
            model_name='subjectrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AddField(
            model_name='transferinrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AddField(
            model_name='transferoutrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AddField(
            model_name='visitrow',
            name='row_comment',
            field=models.ManyToManyField(to='cephia.ImportedRowComment', null=True),
        ),
    ]
