# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_assays(apps, schema_editor):
    model = apps.get_model("cephia", "Assay")

    assay_list = [{'short_name':'LAg-Sedia',
                   'long_name':'Limiting Antigen Assay (Sedia)',
                   'developer':'CDC/Sedia',
                   'description':''},
                  {'short_name':'LAg-Maxim',
                   'long_name':'Limiting Antigen Assay (Maxim)',
                   'developer':'CDC/Maxim',
                   'description':''},
                  {'short_name':'ArchitectUnmodified',
                   'long_name':'Unmodifed ARCHITECT Assay',
                   'developer':'Abbott',
                   'description':''},
                  {'short_name':'ArchitectAvidity',
                   'long_name':'ARCHITECT Avidity Assay',
                   'developer':'Abbott',
                   'description':''},
                  {'short_name':'BioRadAvidity-CDC',
                   'long_name':'BioRad Avidity Assay - Owen Modification',
                   'developer':'CDC/Bi-oRad',
                   'description':''},
                  {'short_name':'BioRadAvidity-JHjU',
                   'long_name':'BioRad Avidity Assay - Layendecker Modification',
                   'developer':'JHU/Bio-Rad',
                   'description':''},
                  {'short_name':'Vitros',
                   'long_name':'Vitros Avidity Assay',
                   'developer':'Vitros',
                   'description':''},
                  {'short_name':'LSVitros-Diluent',
                   'long_name':'Less Sensitive Vitros Assay',
                   'developer':'Vitros',
                   'description':''},
                  {'short_name':'LSVitros-Plasma',
                   'long_name':'Less Sensitive Vitros Assay',
                   'developer':'Vitros',
                   'description':''},
                  {'short_name':'Geenius',
                   'long_name':'Geenius Assay',
                   'developer':'Bio-Rad',
                   'description':''},
                  {'short_name':'BED',
                   'long_name':'BED Assay',
                   'developer':'',
                   'description':''},
                  {'short_name':'BioRadAvidity-Glasgow',
                   'long_name':'BioRad Avidity Assay - Glasgow Modification',
                   'developer':'UGlasgow/Bio-Rad',
                   'description':''},
                  {'short_name':'BioPlex-CDC',
                   'long_name':'BioPlex Assay (CDC)',
                   'developer':'CDC',
                   'description':''},
                  {'short_name':'IDE-iV3',
                   'long_name':'IDE-V3 Assay',
                   'developer':'',
                   'description':''},
                  {'short_name':'BioPlex-Duke',
                   'long_name':'BioPlex Assay (Duke)',
                   'developer':'Duke University',
                   'description':''},
                  {'short_name':'Immunetics-MixL',
                   'long_name':'Immunetics Assay (MixL)',
                   'developer':'Immunetics',
                   'description':''},
                  {'short_name':'Immunetics-NewMix',
                   'long_name':'Immunetics Assay (NewMix)',
                   'developer':'Immunetics',
                   'description':''},
                  {'short_name':'Immunetics-NewMixPeptide',
                   'long_name':'Immunetics Assay (NewMix Peptide)',
                   'developer':'Immunetics',
                   'description':''}]

    for assay in assay_list:
        model.objects.create(name=assay['short_name'],
                             long_name=assay['long_name'],
                             developer=assay['developer'],
                             description=assay['description'])

class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_assays),
    ]
