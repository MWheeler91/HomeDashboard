# Generated by Django 4.2 on 2023-12-06 18:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0010_item_purchase_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='updated_date',
            new_name='last_updated_date',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='updated_time',
            new_name='last_updated_time',
        ),
        migrations.AddField(
            model_name='item',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_entered_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='entered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entered_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
