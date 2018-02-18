from django.urls import path

from todolist.views import index
from todolist import views

urlpatterns = [
    path('', index, name='todolist.index'),
    path('add', views.add_todo, name='add_todo'),
]
