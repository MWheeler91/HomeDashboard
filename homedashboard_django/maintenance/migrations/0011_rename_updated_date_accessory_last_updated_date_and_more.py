# Generated by Django 4.2 on 2023-12-18 20:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maintenance', '0010_rename_entered_date_accessoriesfile_date_entered_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accessory',
            old_name='updated_date',
            new_name='last_updated_date',
        ),
        migrations.RenameField(
            model_name='accessory',
            old_name='updated_time',
            new_name='last_updated_time',
        ),
        migrations.RenameField(
            model_name='maintenance',
            old_name='updated_date',
            new_name='last_updated_date',
        ),
        migrations.RenameField(
            model_name='maintenance',
            old_name='updated_time',
            new_name='last_updated_time',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='updated_date',
            new_name='last_updated_date',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='updated_time',
            new_name='last_updated_time',
        ),
        migrations.AddField(
            model_name='accessory',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='maintenance_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='license_plate_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='accessory',
            name='entered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accessories', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='entered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maintence', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='entered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='VehicleRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_expiration_date', models.DateField(blank=True, null=True)),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('active_year', models.BooleanField()),
                ('date_entered', models.DateField(default=datetime.datetime.now)),
                ('last_updated_date', models.DateField(auto_now=True, null=True)),
                ('last_updated_time', models.TimeField(auto_now=True, null=True)),
                ('entered_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='registration', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='registration_updated', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.vehicle')),
            ],
        ),
    ]