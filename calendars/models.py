from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    added_date = models.DateField(default="2018-01-01")
    added_time = models.TimeField(default="00:00:00:000000")
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_public = models.BooleanField()
    date = models.DateField(default="2018-01-01")
    time = models.TimeField()
    status = models.CharField(max_length=64, default="opened")
