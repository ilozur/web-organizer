# Generated by Django 2.0.2 on 2018-05-06 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20180504_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todos',
            name='smart_priority',
            field=models.IntegerField(default=1),
        ),
    ]
