# Generated by Django 4.2 on 2023-12-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_item_condition_alter_item_item_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='date_updated',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]