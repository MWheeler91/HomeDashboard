# Generated by Django 4.2 on 2025-05-28 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audiowatch', '0004_alter_miceventlog_fk_machine_id_and_more'),
        ('apps', '0008_remove_manageddevice_entered_by_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ManagedDevice',
        ),
        migrations.DeleteModel(
            name='SshKeys',
        ),
    ]
