# Generated by Django 4.2 on 2023-12-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0005_alter_accessory_options_alter_maintenance_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessory',
            name='date_updated',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='date_updated',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='date_updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
