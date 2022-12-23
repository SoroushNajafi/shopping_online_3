# Generated by Django 4.1.3 on 2022-12-21 13:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_category_fa_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='datetime_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='category',
            name='datetime_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
