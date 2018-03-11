from django.db import models
from django.contrib.auth.models import User


class Todos(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    added_time = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=100, default="priority")
    status = models.CharField(max_length=128, default="in progress")
    deadline = models.CharField(max_length=128, default="deadline")
    text = models.CharField(max_length=200, default="time")
    title = models.CharField(max_length=128, default="title")

    @staticmethod
    def get_todos(sorting_type, status, user):
        mode = {
            'AtoZ': 'title',
            'ZtoA': '-title',
            'old': 'added_time',
            'new': '-added_time'
        }
        todos = Todos.objects.filter(user=user, status=status).order_by(mode.get(sorting_type))
        todo_list = list()
        for item in todos:
            todo_list.append((item.title, item.added_time.strftime("%I:%M%p on %B %d, %Y"), item.id))
        return todo_list

    @staticmethod
    def get_todo_by_id(id):
        return Todos.objects.filter(id=id).first()
