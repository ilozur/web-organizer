# Generated by Django 2.0.2 on 2018-03-02 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_auto_20180218_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='is_voise',
            field=models.BooleanField(default=False),
        ),
    ]