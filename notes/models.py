from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    data = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    name = models.CharField(max_length=128, default="title")
    added_time = models.DateField(auto_now_add=True)
