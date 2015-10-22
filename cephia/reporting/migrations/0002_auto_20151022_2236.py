# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='report',
            name='query',
            field=models.TextField(),
        ),
    ]
