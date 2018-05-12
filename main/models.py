from django.db import models
from django.contrib.auth.models import User


class UserAvatar(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    image = models.ImageField(upload_to="avatars/")

    def __init__(self, *args, **kwargs):
        super(UserAvatar, self).__init__(*args, **kwargs)
        self.image.verbose_name = "{}.png".format(self.user.id)


class Language(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    lang = models.CharField(max_length=3, default="ru")


class ConfirmKey(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    key = models.CharField(max_length=256)
    expiration_date = models.DateField(default="2018-01-01")


class ConfirmMailKey(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    key = models.CharField(max_length=256)
    email = models.CharField(max_length=150)


def modification_of_user_data(user, name=None, surname=None, username=None):
    """!
            @brief Function that saves modified user data if it is valid
    """
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
