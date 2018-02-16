from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_public = models.BooleanField()
