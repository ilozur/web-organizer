# Generated by Django 2.0.2 on 2018-02-25 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_signupkey_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupkey',
            name='expiration_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
