# Generated by Django 4.2 on 2025-02-28 01:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error_logging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='error',
            name='error_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
