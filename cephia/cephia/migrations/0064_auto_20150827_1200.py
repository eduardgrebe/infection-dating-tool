# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cephia', '0063_historicalfileinfo_historicalspecimen_historicalsubject_historicalvisit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportedRowComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('resolve_date', models.DateTimeField()),
                ('resolve_action', models.TextField()),
                ('assigned_to', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cephia_importedrow_comment',
            },
        ),
        migrations.AlterField(
            model_name='aliquotrow',
            name='state',
            field=models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')]),
        ),
        migrations.AlterField(
            model_name='subjectrow',
            name='state',
            field=models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')]),
        ),
        migrations.AlterField(
            model_name='transferinrow',
            name='state',
            field=models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')]),
        ),
        migrations.AlterField(
            model_name='transferoutrow',
            name='state',
            field=models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')]),
        ),
        migrations.AlterField(
            model_name='visitrow',
            name='state',
            field=models.CharField(max_length=10, choices=[(b'pending', b'Pending'), (b'validated', b'Validated'), (b'imported', b'Imported'), (b'processed', b'Processed'), (b'error', b'Error')]),
        ),
    ]
