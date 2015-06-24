# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0028_auto_20150616_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='country',
            field=models.ForeignKey(blank=True, to='cephia.Country', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='ethnicity',
            field=models.ForeignKey(blank=True, to='cephia.Ethnicity', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subtype',
            field=models.ForeignKey(blank=True, to='cephia.Subtype', null=True),
        ),
    ]
