from django.db import models


class Creating (models.Model):
    inputfld = models.IntegerField()
    choicebox = models.CharField(max_length=4, choices=(('n', 'Notes'), ('e', 'Events'), ('t', 'Todos'), ('u', 'Users')))

class CreateUsr (models.Model):
    logfld = models.CharField(max_length=40)
    passfld = models.CharField(max_length=40)
    langfld = models.CharField(max_length=3)