# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0073_auto_20150904_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliquotrow',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AddField(
            model_name='subjectrow',
            name='subject',
            field=models.ForeignKey(to='cephia.Subject', null=True),
        ),
        migrations.AddField(
            model_name='transferinrow',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AddField(
            model_name='transferoutrow',
            name='specimen',
            field=models.ForeignKey(to='cephia.Specimen', null=True),
        ),
        migrations.AddField(
            model_name='visitrow',
            name='visit',
            field=models.ForeignKey(to='cephia.Visit', null=True),
        ),
    ]
