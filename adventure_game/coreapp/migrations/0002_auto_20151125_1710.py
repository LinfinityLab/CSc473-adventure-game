#pylint: disable=C0103
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='character_pin',
            field=models.CharField(max_length=200, null=True),
        ),
    ]