from django.urls import path
from todo import views
from todo.views import *

urlpatterns = [
    path('', views.index, name='todo.index'),
    path('edit', views.edit_todo, name='todo.edit_todo'),
    path('show_todo', views.show_todo, name='todo.show_todo'),
    path('add', views.add_todo, name='todo.add_todo'),
    path('search', views.search, name='todo.search'),
    path('sort', views.sorting, name='todo.sort'),
    path('delete', views.delete_todo, name='todo.delete_todo'),
    path('latest',get_latest_todo, name= 'todo.latest')
]
