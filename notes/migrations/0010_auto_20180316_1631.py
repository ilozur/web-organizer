# Generated by Django 2.0.2 on 2018-03-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0009_auto_20180315_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='added_time',
            field=models.DateTimeField(default=None),
        ),
    ]