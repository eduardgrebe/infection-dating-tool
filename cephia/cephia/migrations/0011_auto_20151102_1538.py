# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0010_auto_20151028_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='cephiauser',
            name='num_login_failures',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='cephiauser',
            name='temporary_locked_out_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='cephiauser',
            name='created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='cephiauser',
            name='modified',
            field=models.DateTimeField(),
        ),
    ]
