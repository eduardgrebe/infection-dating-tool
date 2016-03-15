# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_panels(apps, schema_editor):

    model = apps.get_model("cephia", "Panel")
    specimen_type_model = apps.get_model("cephia", "SpecimenType")
    panel_file = open('cephia/migrations/panel_list.csv')
    headers = panel_file.readline().strip().split(',')

    for row in panel_file.readlines():
        panel = dict(zip(headers, row.strip().split(',')))
        model.objects.create(short_name=panel['short_name'],
                             name=panel['name'],
                             description=panel['description'],
                             specimen_type=specimen_type_model.objects.get(pk=panel['specimen_type_id']),
                             n_recent=panel['n_recent'] or None,
                             n_longstanding=panel['n_longstanding'] or None,
                             n_challenge=panel['n_challenge'] or None,
                             n_reproducibility_controls=panel['n_reproducibility_controls'] or None,
                             n_negative=panel['n_negative'] or None,
                             n_total=panel['n_total'] or None,
                             blinded=panel['blinded'],
                             notes=panel['notes'])

class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0031_auto_20160315_1540'),
    ]

    operations = [
        migrations.RunPython(add_panels),
    ]
