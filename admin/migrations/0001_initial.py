# Generated by Django 2.0.5 on 2018-05-18 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreateUsr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logfld', models.CharField(max_length=40)),
                ('passfld', models.CharField(max_length=40)),
                ('langfld', models.CharField(max_length=3)),
                ('key', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Creating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inputfld', models.IntegerField()),
                ('checkbox', models.BooleanField()),
                ('key', models.CharField(max_length=2)),
            ],
        ),
    ]
