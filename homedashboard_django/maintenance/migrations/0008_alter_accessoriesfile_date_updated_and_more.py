# Generated by Django 4.2 on 2023-12-06 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0007_accessoriesfile_date_entered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessoriesfile',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='accessory',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='maintenancefile',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
