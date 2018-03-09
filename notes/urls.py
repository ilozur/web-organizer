from django.urls import path

from notes.views import *

urlpatterns = [
    path('', index, name='notes.index'),
    path('add', add_note, name='notes.add_note'),
    path('show/<int:id>', show_note, name='notes.show_note'),
    path('search', search_ajax, name='notes.search'),
    path('sort', sort_ajax, name='notes.sort'),
]
