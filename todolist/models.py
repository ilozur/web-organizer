from django.db import models
from django.contrib.auth.models import User


class Todos(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    added_time = models.CharField(max_length=25, default=0)
    priority = models.CharField(max_length=1, default="priority")
    status = models.CharField(max_length=128, default="status")
    deadline = models.CharField(max_length=128, default="deadline")