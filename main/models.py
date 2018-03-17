from django.db import models
from django.contrib.auth.models import User


class SignUpKey(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    key = models.CharField(max_length=256)
    expiration_date = models.DateField(default="2018-01-01")


def modification_of_user_data(user, name=None, surname=None, username=None):
    if name is not None:
        user.first_name = name
    if surname is not None:
        user.last_name = surname
    user.save()
    if username is not None:
        if User.objects.filter(username=username).count() == 0:
            user.username = username
            user.save()
        else:
            return False
    return True


class ConfirmMailKey(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    key = models.CharField(max_length=256)
    email = models.CharField(max_length=150)


class RecoverPasswordKey(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    key = models.CharField(max_length=256)
    expiration_date = models.DateField(default="2018-01-01")
