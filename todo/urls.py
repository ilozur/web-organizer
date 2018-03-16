from django.urls import path
from todo.views import index
from todo import views

urlpatterns = [
    path('', index, name='todo.index'),
    path('completed', views.completed_todos, name='todo.completed_todos'),
    path('show/<int:id>', views.show_todo, name='todo.show_todo'),
    path('saving', views.save_todo, name='todo.save_todo'),
    path('sort', views.sorting, name='sort'),
    path('change', views.status_change, name='change'),
]
