from django.urls import path
from notes.views import *

urlpatterns = [
    path('', index, name="notes.index"),
    #path('save', save_ajax, name='notes.save'),
    path('get_note_data', get_note_data, name='notes.get_note_data'),
    #path('add', add_note_ajax, name='notes.add'),
    path('search', search, name='notes.search'),
    path('delete', delete_note, name='notes.delete'),
    path('sort', sort_notes, name='notes.sort'),
]
