# Generated by Django 2.0.8 on 2018-11-09 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UCSDMarket', '0002_auto_20181109_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='picture',
            field=models.ImageField(upload_to='pictures/'),
        ),
    ]
