# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_ethnicities(apps, schema_editor):

    model = apps.get_model("cephia", "Ethnicity")

    ethnicities = ['Hispanic/Latino',
                   'Black African',
                   'Brazilian',
                   'Multiethnic',
                   'African American',
                   'White',
                   'Other',
                   'Unknown',
                   'Asian']

    for ethnicity in ethnicities:
        model.objects.create(name=ethnicity)

class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0047_auto_20150622_1230'),
    ]

    operations = [
        migrations.RunPython(add_ethnicities),
    ]
