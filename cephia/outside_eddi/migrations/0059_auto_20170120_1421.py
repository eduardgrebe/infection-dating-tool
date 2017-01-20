# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-20 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outside_eddi', '0058_auto_20161209_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaloutsideeddidiagnostictest',
            name='description',
        ),
        migrations.RemoveField(
            model_name='outsideeddidiagnostictest',
            name='description',
        ),
        migrations.AddField(
            model_name='historicaloutsideeddidiagnostictest',
            name='category',
            field=models.CharField(blank=True, choices=[('1st_gen', '1st Gen Lab Assay (Viral Lysate IgG sensitive Antibody)'), ('2nd_gen_lab', '2nd Gen Lab Assay (Recombinant IgG sensitive Antibody)'), ('2nd_gen_rapid', '2nd Gen Rapid Test'), ('3rd_gen_lab', '3rd Gen Lab Assay (IgM sensitive Antibody)'), ('3rd_gen_rapid', '3rd Gen Rapid Test'), ('4th_gen_lab', '4th Gen Lab Assay (p24 Ag/Ab Combo)'), ('4th_gen_rapid', '4th Gen Rapid Test'), ('dpp', 'DPP'), ('immunofluorescence_assay', 'Immunofluorescence Assay'), ('p24_antigen', 'p24 Antigen'), ('viral_load', 'Viral Load'), ('western_blot', 'Western Blot')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='outsideeddidiagnostictest',
            name='category',
            field=models.CharField(blank=True, choices=[('1st_gen', '1st Gen Lab Assay (Viral Lysate IgG sensitive Antibody)'), ('2nd_gen_lab', '2nd Gen Lab Assay (Recombinant IgG sensitive Antibody)'), ('2nd_gen_rapid', '2nd Gen Rapid Test'), ('3rd_gen_lab', '3rd Gen Lab Assay (IgM sensitive Antibody)'), ('3rd_gen_rapid', '3rd Gen Rapid Test'), ('4th_gen_lab', '4th Gen Lab Assay (p24 Ag/Ab Combo)'), ('4th_gen_rapid', '4th Gen Rapid Test'), ('dpp', 'DPP'), ('immunofluorescence_assay', 'Immunofluorescence Assay'), ('p24_antigen', 'p24 Antigen'), ('viral_load', 'Viral Load'), ('western_blot', 'Western Blot')], max_length=255, null=True),
        ),
    ]
