# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-10-20 10:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import lib.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('outside_eddi', '0024_auto_20161020_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaloutsideedditestpropertyestimate',
            name='user',
            field=lib.fields.ProtectedForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='outsideedditestpropertyestimate',
            name='user',
            field=lib.fields.ProtectedForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]