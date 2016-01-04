# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_assays(apps, schema_editor):
    model = apps.get_model("cephia", "Assay")
    
    assay_list = [{'short_name':'LAg',
                   'long_name':'Limiting Antigen Assay',
                   'developer':'CDC/Sedia',
                   'description':''},
                  {'short_name':'Architect',
                   'long_name':'Architect Avidity Assay',
                   'developer':'Abbott',
                   'description':''},
                  {'short_name':'BioRad-Avidity-CDC',
                   'long_name':'BioRad Avidity Assay - Owen Modification',
                   'developer':'CDC/BioRad',
                   'description':''},
                  {'short_name':'BioRad-Avidity-JHU',
                   'long_name':'BioRad Avidity Assay - Layendecker Modification',
                   'developer':'JHU/BioRad',
                   'description':''},
                  {'short_name':'Vitros',
                   'long_name':'Vitros Avidity Assay',
                   'developer':'Vitros',
                   'description':''},
                  {'short_name':'LS-Vitros',
                   'long_name':'Less Sensitive Vitros Assay',
                   'developer':'Vitros',
                   'description':''},
                  {'short_name':'Geenius',
                   'long_name':'Geenius Assay (Company?)',
                   'developer':'',
                   'description':''},
                  {'short_name':'BED',
                   'long_name':'??',
                   'developer':'',
                   'description':''},
                  {'short_name':'BioRad-Avidity-Glasgow',
                   'long_name':'BioRad Avidity Assay - Glasgow Modification',
                   'developer':'',
                   'description':''},
                  {'short_name':'Luminex',
                   'long_name':'Luminex Assay (??)',
                   'developer':'',
                   'description':''},
                  {'short_name':'IDE-V3',
                   'long_name':'IDE-V3 Assay',
                   'developer':'',
                   'description':''},
                  {'short_name':'Duke-BioPlex',
                   'long_name':'?? (Duke University)',
                   'developer':'',
                   'description':''}]


    for assay in assay_list:
        model.objects.create(short_name=assay['short_name'],
                             long_name=assay['long_name'],
                             developer=assay['developer'],
                             description=assay['description'])
        
class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0016_auto_20160101_1241'),
    ]

    operations = [
        migrations.RunPython(add_assays),
    ]

