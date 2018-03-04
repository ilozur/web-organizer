from django.db import models
from django.contrib.auth.models import User


class Todos(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    added_time = models.TimeField(max_length=20, default='2018-01-01')
    added_date = models.DateField(max_length=20, default='00-00')
    priority = models.CharField(max_length=100, default="priority")
    status = models.CharField(max_length=128, default="in progress")
    deadline = models.CharField(max_length=128, default="deadline")
    text = models.CharField(max_length=200, default="time")
    title = models.CharField(max_length=128, default="title")

    @staticmethod
    def get_todos(sorting_type, user=1):
        # if aim = 'date' -> 'up' = new-old, 'down' = old-new
        # if aim = 'title' -> 'up' = a-z, 'down' = z-a
        todos = Todos.objects.filter(user=user)
        if sorting_type != 'all':
            direction = sorting_type
        else:
            return todos
        if direction == "AtoZ":
            todos = todos.order_by('-added_time')
        elif direction == "ZtoA":
            todos = todos.order_by('added_time')
        if direction == "new":
            todos = todos.order_by('title')
        elif direction == "old":
            todos = todos.order_by('-title')
        return todos
