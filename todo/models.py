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
    def delete_todo(todo_id, user):
        """
        @param
        This is ID of todos
        @brief
        This function deletes todo
        """
        todos = Todos.objects.filter(user=user, id=todo_id)
        if len(todos) > 0:
            fully_deleted = False
            if todos[0].folder:
                if todos[0].folder.done:
                    todos[0].delete()
                    fully_deleted = True
            if not fully_deleted:
                done_folder = TodosFolder.objects.filter(user=user, done=True)
                if len(done_folder) == 0:
                    tmp_folder = TodosFolder(user=user, title="Recently deleted", done=True)
                    tmp_folder.save()
                done_folder = TodosFolder.objects.filter(user=user, done=True)
                todos[0].folder = done_folder[0]
                todos[0].save()
            return 100
        else:
            return 111

    @staticmethod
    def search_todos(aim, user, sorting_type="date_up", folder=None):
        """
        @brief
        This function searches for the todos
        """
        todos = Todos.get_todos(sorting_type, user, folder=folder)
        if aim is None:
            aim = ""
        todos = todos.filter(title__icontains=aim)
        return todos