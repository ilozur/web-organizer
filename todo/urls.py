from django.urls import path
from todo import views

urlpatterns = [
    path('edit', views.edit_todo, name='todo.edit_todo'),
    path('show_todo', views.show_todo, name='todo.show_todo'),
    path('add', views.add_todo, name='todo.add_todo'),
    path('search', views.search, name='todo.search'),
    path('sort', views.sorting, name='todo.sort'),
    path('change', views.status_change, name='todo.change'),
    path('delete', views.delete_todo, name='todo.delete_todo'),
    path('paginate', views.paginate, name='todo.paginate')
]
