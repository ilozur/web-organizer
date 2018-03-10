from django.urls import path

from notes.views import *

urlpatterns = [
    path('', index, name='notes.index'),
    path('show/<int:id>', show_note, name='notes.show_note'),
    path('save', save_ajax, name='notes.save'),
    path('add', add_note_ajax, name='notes.add'),
    path('search', search_ajax, name='notes.search'),
    path('sort', sort_ajax, name='notes.sort'),
]
