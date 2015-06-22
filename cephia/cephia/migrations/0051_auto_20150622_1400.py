# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_sites(apps, schema_editor):

    model = apps.get_model("cephia", "Site")

    sites = ['PHE',
             'BSRI']

    for site in sites:
        model.objects.create(name=site)


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0050_specimen_site'),
    ]

    operations = [
        migrations.RunPython(add_sites),
    ]
