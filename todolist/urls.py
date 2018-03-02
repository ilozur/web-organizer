from django.urls import path

from todolist.views import index
from todolist import views

urlpatterns = [
    path('', index, name='todolist.index'),

    path('add', views.add_todo, name='todolist.add_todo'),
    path('done', views.completed_todos, name='todolist.completed_todos'),
    path('add', add_todolist, name='todolist.add_todolist'),
    path('show/<int:id>', show_todolist, name='todo.show_todolist'),
]
