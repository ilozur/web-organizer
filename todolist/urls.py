from django.urls import path

from todolist.views import index
from todolist import views

urlpatterns = [
    path('', index, name='todolist.index'),
    path('completed', views.completed_todos, name='todolist.completed_todos'),
    path('show/<int:id>', views.show_todo, name='todolist.show_todo'),
    path('saving',views.save_todo, name='todolst.save_todo'),
    path('sort', views.sort_ajax, name='sort'),
    path('add', views.add_todo, name='todolist.add_todolist'),
]
