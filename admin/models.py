from django.db import models

class User(models.Model):
    userName = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    surename = models.CharField(max_length=128)
    added_time = models.DateTimeField(auto_now_add=True)
    is_voice = models.BooleanField(default=False)
    last_edit_time = models.DateTimeField(default=None, null=True)


def get_users():
    users = User.objects.all()

