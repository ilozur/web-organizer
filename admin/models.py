from django.db import models


class Creating (models.Model):
    inputfld = models.IntegerField(max_length=3)
    checkbox = models.BooleanField()
    btnsubmit = models.CharField(max_length=2)

class CreateUsr (models.Model):
    logfld = models.CharField(max_length=40)
    passfld = models.CharField(max_length=40)
    langfld = models.CharField(max_length=3)
