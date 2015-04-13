# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.core.management import call_command
import os


def init_data(apps, schema_editor):
    call_command('loaddata', os.path.join('..', 'fixtures', 'data.json'))

class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_data)
    ]

