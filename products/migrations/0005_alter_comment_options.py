# Generated by Django 4.1.3 on 2022-11-26 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_comment_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-datetime_created',)},
        ),
    ]
