# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0004_diagnostictesthistoryrow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testpropertyestimate',
            name='description',
        ),
        migrations.AddField(
            model_name='testpropertyestimate',
            name='comment',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='testpropertyestimate',
            name='estimate_label',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='testpropertyestimate',
            name='reference',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
