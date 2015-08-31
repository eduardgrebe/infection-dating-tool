# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0067_auto_20150831_1012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aliquotrow',
            name='row_comment',
        ),
        migrations.RemoveField(
            model_name='subjectrow',
            name='row_comment',
        ),
        migrations.RemoveField(
            model_name='transferinrow',
            name='row_comment',
        ),
        migrations.RemoveField(
            model_name='transferoutrow',
            name='row_comment',
        ),
        migrations.RemoveField(
            model_name='visitrow',
            name='row_comment',
        ),
        migrations.AddField(
            model_name='aliquotrow',
            name='comment',
            field=models.ForeignKey(to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AddField(
            model_name='subjectrow',
            name='comment',
            field=models.ForeignKey(to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AddField(
            model_name='transferinrow',
            name='comment',
            field=models.ForeignKey(to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AddField(
            model_name='transferoutrow',
            name='comment',
            field=models.ForeignKey(to='cephia.ImportedRowComment', null=True),
        ),
        migrations.AddField(
            model_name='visitrow',
            name='comment',
            field=models.ForeignKey(to='cephia.ImportedRowComment', null=True),
        ),
    ]
