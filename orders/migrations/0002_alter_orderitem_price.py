# Generated by Django 4.1.3 on 2023-01-31 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
