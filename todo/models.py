from django.db import models
from django.contrib.auth.models import User


class Todos(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    added_date_and_time = models.DateTimeField(auto_now_add=True)
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
        if sorting_type == 'all':
            todos = Todos.objects.filter(user=user)
        elif sorting_type in mode.keys():
            todos = Todos.objects.filter(user=user).order_by(mode.get(sorting_type))
        if status is not None:
            todos.filter(status=status)
        return todos

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
        obj = Todos.get_todos('all', None, user)
        ret_list = list()
        for i in obj:
            if string in i.title:
                ret_list.append((i.title, i.added_date_and_time.strftime("%I:%M%p on %B %d, %Y"), i.id))
        return ret_list

    @staticmethod
    def todos_sort_by_date(datetime, user):  # todos: datetime = {1: date_one NOT NULL, 2: date_two}
        todolist = Todos.objects.filter(user=user)
        if len(datetime) == 1:
            date = datetime[0].date()
            return todolist.filter(pub_date=date)
        else:
            return todolist.filter(pub_date__gte=datetime[0].date(),
                                   pub_date__lte=datetime[1].date()).order_by('-pub_date')
