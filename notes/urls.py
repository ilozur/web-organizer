from django.urls import path
from notes.views import *

urlpatterns = [
    path('', index, name="notes.index"),
    path('save', save_note, name='notes.save'),
    path('get_note_data', get_note_data, name='notes.get_note_data'),
    path('delete', delete_note, name='notes.delete'),
    path('sort', sort, name='notes.sort'),
    path('get_folder', get_folder, name='notes.get_folder'),
    path('search', search, name='notes.search')
]
