# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.db import migrations


def load_fixtures(apps, schema_editor):
    call_command('loaddata', 'rollingstock.json')
    call_command('loaddata', 'lines.json')


def remove_fixture(apps, schema_editor):
    call_command('flush')


class Migration(migrations.Migration):

    dependencies = [
        ('metroapp', '0001_initial')
    ]

    operations = [
        migrations.RunPython(
            load_fixtures,
            reverse_code=remove_fixture),
    ]
