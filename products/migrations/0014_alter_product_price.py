# Generated by Django 4.1.3 on 2023-01-31 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
