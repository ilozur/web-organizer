from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json

from notes.forms import *
from notes.models import Notes

from datetime import datetime

from django.core.paginator import Paginator

from main.views import get_language


@login_required
def index(request):
    if request.method == "GET":
        notes = Notes.get_notes("date_up", request.user)
        context = dict()
        context['title'] = "Notes index page"
        context['lang'], context['language'] = get_language(request)
        notes_titles = [note.name for note in notes]
        pages = Paginator(notes_titles, 20)

        context['all_notes_count'] = len(notes)
        context['voice_notes_count'] = len(notes.filter(is_voice=True))
        context['text_notes_count'] = int(context['all_notes_count']) - int(context['voice_notes_count'])

        context['notes'] = pages.page(1)
        context['search_note_form'] = SearchForm()
        context['add_note_form'] = AddNoteForm()
        context['edit_note_form'] = EditNoteForm()
        return render(request, "notes/index.html", context)
