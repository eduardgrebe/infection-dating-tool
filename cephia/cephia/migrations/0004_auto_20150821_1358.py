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

    source_study_list = [{'name':'SIPP',
                          'description':'Options study - SIPP samples (large volume collections)'},
                         {'name':'ARCHIVE',
                          'description':'Options study - Archive samples (remnants from the old archive)'},
                         {'name':'IAVI',
                          'description':'IAVI study - from core lab in London'},
                         {'name':'UCSD',
                          'description':'UCSD study, San Diego, CA'},
                         {'name':'SCOPE',
                          'description':'SCOPE study, San Francisco, CA'},
                         {'name':'AMPLIAR',
                          'description':'AMPLIAR study, Brazil'},
                         {'name':'SFMHS',
                          'description':'San Francisco Men’s Health Study'},
                         {'name':'CTS',
                          'description':'Blood bank - ARC/MS (American Red Cross)'},
                         {'name':'BCP',
                          'description':'Blood bank - Blood Centers of the Pacific (BSRI)'},
                         {'name':'BRAZIL',
                          'description':'Blood bank - Brazil'},
                         {'name':'SANBS',
                          'description':'Blood bank  - SANBS'},
                         {'name':'CAPRISA',
                          'description':'CAPRISA study – South Africa'},
                         {'name':'FPSHSP',
                          'description':'Fundação Pro-Sangue-Hemocentro de São Paulo, Brazil'},
                         {'name':'GAMA',
                          'description':'CRESIB malaria cohort'},
                         {'name':'IMPACTA',
                          'description':'Asociación Civil Impacta Saludy Educación'}]


    for study in source_study_list:
        model.objects.create(name=study['name'], description=study['description'])

class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0003_auto_20150821_1358'),
    ]

    operations = [
        migrations.RunPython(add_locations_studies),
    ]
