# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iframeapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apikey',
            name='id',
        ),
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(max_length=50, serialize=False, editable=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='apikey',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
