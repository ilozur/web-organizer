from django.urls import path

from todolist.views import index

urlpatterns = [
    path('', index, name='todolist.index'),
    path('add', add_todolist, name='todolist.add_todolist'),
    path('show/<int:id>', show_todolist, name='todo.show_todolist'),
]
