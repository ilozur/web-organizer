# Generated by Django 2.0.2 on 2018-05-20 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calendars', '0008_auto_20180422_0021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='is_public',
            new_name='is_private',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='place',
            new_name='location',
        ),
    ]
