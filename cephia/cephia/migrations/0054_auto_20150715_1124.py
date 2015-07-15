# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
def add_locations(apps, schema_editor):

    model = apps.get_model("cephia", "Location")

    locations = ['PHE',
                 'BSRI']

    for location in locations:
        model.objects.create(name=location)


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0053_auto_20150624_2152'),
    ]

    operations = [
        migrations.RunPython(add_locations),
    ]

