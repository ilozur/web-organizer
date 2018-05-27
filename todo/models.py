import datetime

from django.db import models
from django.contrib.auth.models import User


class TodosFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Title")
    done = models.BooleanField(default=False)


class Todos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="title")
    added_time = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(default=3)
    status = models.CharField(max_length=128, default="in progress")
    deadline = models.DateTimeField(default='2018-06-01 00:00')
    folder = models.ForeignKey(TodosFolder, on_delete=models.CASCADE, default=None, null=True)

    @staticmethod
    def get_todos(sorting_type, user=None, todos=None, folder=None):
        """
            @brief
            This function get todos
            @detailed
            This function get todos by time and alphabetically
            if aim = 'date' -> 'up' = new-old, 'down' = old-new
            if aim = 'title' -> 'up' = a-z, 'down' = z-a
            if sorting type is not correct returns returns todos sorted like date_up
        """
        if user is None:
            return None
        if todos is None:
            todos = Todos.objects.filter(user=user)
        todos = todos.filter(user=user).order_by('-added_time')
        sorting_types = ['date_up', 'date_down', 'title_up', 'title_down', 'all']
        if sorting_type not in sorting_types:
            sorting_type = "date_up"
        if sorting_type != 'all':
            sort = sorting_type.split('_')
            aim = sort[0]
            direction = sort[1]
        else:
            return todos
        if aim == "date":
            if direction == "up":
                todos = todos.order_by('-added_time')
            elif direction == "down":
                todos = todos.order_by('added_time')
            else:
                return todos
        elif aim == "title":
            if direction == "up":
                todos = todos.order_by('title')
            elif direction == "down":
                todos = todos.order_by('-title')
            else:
                return todos
        else:
            return todos
        done_folder = TodosFolder.objects.filter(user=user, done=True)
        if len(done_folder) == 0:
            tmp_folder = TodosFolder(user=user, title="Done", done=True)
            tmp_folder.save()
        done_folder = TodosFolder.objects.filter(user=user, done=True)
        if folder is None:
            todos = todos.exclude(folder=done_folder[0])
        else:
            todos = todos.filter(folder=folder)
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
