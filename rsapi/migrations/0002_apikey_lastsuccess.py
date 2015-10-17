# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='lastSuccess',
            field=models.DateTimeField(null=True),
        ),
    ]
