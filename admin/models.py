from django.db import models


class Creating (models.Model):
    inputfld = models.IntegerField(max_length=3)
    checkbox = models.BooleanField()
    btnsubmit = models.TextField(max_length=2)
