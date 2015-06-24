# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_locations_studies(apps, schema_editor):

    model = apps.get_model("cephia", "Location")

    locations = ['MAX',
                 'META',
                 'BGI',
                 'USC',
                 'SBS',
                 'KEM',
                 'CEK',
                 'Duke',
                 'Pitt',
                 'Roederer',
                 'Metabolistics']

    for location in locations:
        model.objects.create(name=location)


    model = apps.get_model("cephia", "Study")

    studies = ['UCSD',
               'BRAZIL',
               'IMPACTA',
               'ARC/MS',
               'CAPRISA',
               'SANBS',
               'ARCHIVE',
               'BCP',
               'GAMA',
               'SCOPE',
               'SIPP',
               'CORE LAB',
               'AMPLIAR',
               'SFMHS']

    for study in studies:
        model.objects.create(name=study)

class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0045_auto_20150621_1853'),
    ]

    operations = [
        migrations.RunPython(add_locations_studies),
    ]
