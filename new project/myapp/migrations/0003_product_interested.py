# Generated by Django 5.1.5 on 2025-03-01 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_category_warehouse_product_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
