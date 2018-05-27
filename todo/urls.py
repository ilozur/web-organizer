from django.urls import path
from todo.views import *

urlpatterns = [
    path('', index, name='todo.index'),
    path('save', save_todo, name='todo.save'),
    path('get_note_data', get_todo_data, name='todo.get_todo_data'),
    path('delete', delete_todo, name='todo.delete'),
    path('sort', sort, name='todo.sort'),
    path('get_folder', get_folder, name='todo.get_folder'),
    path('search', search, name='todo.search')
]
