from django.urls import path

from notes.views import *

urlpatterns = [
    path('', index, name='notes.index'),
    path('show/<int:id>', show_note, name='notes.show_note'),
    path('search', search_ajax, name='search'),
    path('sort', sort_ajax, name='sort'),
    path('save', save_ajax, name='save'),
]
