# Generated by Django 2.0.8 on 2018-11-11 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UCSDMarket', '0004_auto_20181110_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='seller',
        ),
    ]
