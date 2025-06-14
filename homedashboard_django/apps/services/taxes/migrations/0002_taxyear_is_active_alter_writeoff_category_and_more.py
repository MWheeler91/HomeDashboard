# Generated by Django 4.2 on 2025-05-26 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_category_is_catalog_category_is_maint_and_more'),
        ('taxes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxyear',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='writeoff',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.category'),
        ),
        migrations.AlterField(
            model_name='writeoff',
            name='tax_year',
            field=models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='taxes.taxyear'),
        ),
        migrations.DeleteModel(
            name='WriteOffCategory',
        ),
    ]
