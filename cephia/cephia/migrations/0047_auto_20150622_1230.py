# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0046_auto_20150622_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='source',
        ),
        migrations.AddField(
            model_name='visit',
            name='study',
            field=models.ForeignKey(blank=True, to='cephia.Study', null=True),
        ),
        migrations.DeleteModel(
            name='Source',
        ),
    ]
