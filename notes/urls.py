from django.urls import path
from notes.views import *

urlpatterns = [
    path('save', save_ajax, name='notes.save'),
    path('get_note_data', get_note_data_ajax, name='notes.get_note_data'),
    path('add', add_note_ajax, name='notes.add'),
    path('search', search_ajax, name='notes.search'),
    path('delete', delete_ajax, name='notes.delete'),
]
