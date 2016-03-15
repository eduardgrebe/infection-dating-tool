# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assay', '0008_auto_20160313_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='panelmembership',
            name='category',
            field=models.CharField(blank=True, max_length=255, choices=[(b'mdri', b'MDRI'), (b'frr', b'FRR'), (b'challenge', b'Challenge')]),
        ),
        migrations.AddField(
            model_name='panelmembership',
            name='panel_inclusion_criterion',
            field=models.CharField(blank=True, max_length=255, choices=[(b'recent_infection_art_naive', b'Recent Infection ART Naive'), (b'longstanding_infection_art_naive', b'Longstanding Infection ART Naive'), (b'recent_infection_art_surpressed', b'Recent Infection ART Surpressed'), (b'longstanding_infection_art_surpressed', b'Longstanding Infection ART Surpressed'), (b'recent_infection_art_unsurpressed', b'Recent Infection ART Unsurpressed'), (b'longstanding_infection_art_unsurpressed', b'Longstanding Infection ART Unsurpressed'), (b'recent_infection_ec', b'Recent Infection Elite Controller'), (b'longstanding_infection_ec', b'Longstanding Infection Elite Controller')]),
        ),
        migrations.AddField(
            model_name='panelmembership',
            name='replicates',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='panelmembershiprow',
            name='category',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='panelmembershiprow',
            name='panel_inclusion_criterion',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='panelmembershiprow',
            name='replicates',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
