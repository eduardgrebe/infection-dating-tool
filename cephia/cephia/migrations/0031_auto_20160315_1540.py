# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0030_auto_20160309_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='panel',
            name='blinded',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_challenge',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_longstanding',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_negative',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_recent',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_reproducibility_controls',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='n_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='notes',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='panel',
            name='short_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
