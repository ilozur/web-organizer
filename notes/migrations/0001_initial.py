<<<<<<< HEAD
# Generated by Django 2.0.2 on 2018-03-16 16:28
=======
# Generated by Django 2.0.2 on 2018-03-18 09:34
>>>>>>> develop

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
<<<<<<< HEAD
                ('name', models.CharField(default='title', max_length=128)),
                ('added_time', models.DateTimeField(auto_now_add=True)),
                ('is_voice', models.BooleanField(default=False)),
=======
                ('name', models.CharField(default='title', max_length=19)),
                ('added_time', models.DateTimeField(default=None)),
                ('is_voice', models.BooleanField(default=False)),
                ('data_part', models.TextField(default='...', max_length=128)),
>>>>>>> develop
                ('last_edit_time', models.DateTimeField(default=None)),
                ('user', models.ForeignKey(default=1, on_delete={1}, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
