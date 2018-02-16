from django.urls import path

from notes.views import index, add_note

urlpatterns = [
    path('', index, name='notes.index'),
    path('add', add_note, name='notes.add_note'),
]
