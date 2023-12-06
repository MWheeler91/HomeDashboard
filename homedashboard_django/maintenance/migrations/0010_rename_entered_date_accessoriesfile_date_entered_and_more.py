# Generated by Django 4.2 on 2023-12-06 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0009_rename_date_entered_accessoriesfile_entered_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accessoriesfile',
            old_name='entered_date',
            new_name='date_entered',
        ),
        migrations.RenameField(
            model_name='accessory',
            old_name='entered_date',
            new_name='date_entered',
        ),
        migrations.RenameField(
            model_name='maintenance',
            old_name='entered_date',
            new_name='date_entered',
        ),
        migrations.RenameField(
            model_name='maintenancefile',
            old_name='entered_date',
            new_name='date_entered',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='entered_date',
            new_name='date_entered',
        ),
        migrations.RemoveField(
            model_name='accessoriesfile',
            name='entered_time',
        ),
        migrations.RemoveField(
            model_name='accessory',
            name='entered_time',
        ),
        migrations.RemoveField(
            model_name='maintenance',
            name='entered_time',
        ),
        migrations.RemoveField(
            model_name='maintenancefile',
            name='entered_time',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='entered_time',
        ),
    ]
