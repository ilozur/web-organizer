from django.db import models
import sqlite3
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    data = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    name = models.CharField(max_length=128, default="title")
    added_time = models.CharField(max_length=25, default=0)

