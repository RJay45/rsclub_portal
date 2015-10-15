# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField()),
                ('userId', models.CharField(max_length=255)),
                ('authKey', models.CharField(max_length=255)),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
            ],
        ),
    ]
