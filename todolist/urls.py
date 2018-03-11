from django.urls import path
from todolist.views import index
from todolist import views

urlpatterns = [
    path('', index, name='todolist.index'),
    path('completed', views.completed_todos, name='todolist.completed_todos'),
    path('show/<int:id>', views.show_todo, name='todolist.show_todo'),
    path('saving',views.save_todo, name='todolist.save_todo'),
    path('sort', views.sorting, name='sort'),
    path('change', views.status_change, name='change'),
]
