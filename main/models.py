from django.db import models
from django.contrib.auth.models import User


class SignUpKey(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    key = models.CharField(max_length=256)
    expiration_date = models.DateField(default="2018-01-01")

 def modification_of_user_data(user, name=None, surname=None, username=None):
        if name != None:
            user.name = name
        if surname != None:
            user.surname = surname
        if username != None:
            user.username = username
