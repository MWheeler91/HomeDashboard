# Generated by Django 4.2 on 2024-07-15 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0013_remove_maintenance_short_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='maintenance',
            name='short_description',
            field=models.CharField(default='n/a', max_length=50),
        ),
    ]
