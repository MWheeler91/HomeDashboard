# Generated by Django 4.2 on 2025-02-28 01:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('error_logging', '0002_error_error_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error',
            name='error_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
