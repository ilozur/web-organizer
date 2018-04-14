import datetime

from django.db import models
from django.contrib.auth.models import User


class Todos(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    title = models.CharField(max_length=128, default="title")
    text = models.CharField(max_length=600, default="time")
    added_date_and_time = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=3)
    status = models.CharField(max_length=128, default="in progress")
    deadline = models.DateField(default=None)

    @staticmethod
    def get_todos(sorting_type, status, user):
        mode = {
            'AtoZ': 'title',
            'ZtoA': '-title',
            'old': 'added_date_and_time',
            'new': '-added_date_and_time'
        }
        todos = Todos.objects.filter(user=user, status=status).order_by(mode.get(sorting_type))
        todo_list = list()
        for item in todos:
            todo_list.append((item.title, item.added_date_and_time.strftime("%I:%M%p on %B %d, %Y"), item.id, item.priority))
        return todo_list

    @staticmethod
    def get_todo_by_id(id):
        if Todos.objects.filter(id=id).count() > 0:
            return Todos.objects.filter(id=id).first()
        else:
            return False

    @staticmethod
    def delete_todo(id):
        if len(Todos.objects.filter(id=id)) > 0:
            Todos.objects.filter(id=id).delete()
            return True
        else:
            return False

    @staticmethod
    def search_todos(string, user):
        obj = Todos.objects.filter(user=user)
        ret_list = list()
        for i in obj:
            if string in i.title:
                ret_list.append((i.title, i.added_date_and_time.strftime("%I:%M%p on %B %d, %Y"), i.id, i.priority))
        return ret_list

    @staticmethod
    def get_amounts(user):
        every = Todos.objects.filter(user=user).count()
        undone = Todos.objects.filter(status='in progress', user=user).count()
        return [every, undone, (every - undone)]
