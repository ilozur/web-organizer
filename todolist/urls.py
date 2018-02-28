from django.urls import path

from todolist.views import index
from todolist import views

urlpatterns = [
    path('', index, name='todolist.index'),
    path('add', views.add_todo, name='todolist.add_todo'),
    path('done', views.completed_todos, name='todolist.completed_todos'),
    path('add', views.add_todo, name='add_todo'),
    path('show/<int:id>', views.show_todo, name='show_todo')
]
