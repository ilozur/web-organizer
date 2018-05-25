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
        if len(notes) > 0:
            context['notes'] = notes
            context['no_notes'] = False
        else:
            context['no_notes'] = True
        context['search_note_form'] = SearchForm()
        context['add_note_form'] = AddNoteForm()
        context['edit_note_form'] = EditNoteForm()
        return render(request, "notes/index.html", context)


def create_added_date(lang, real_time):
    """
    @brief
    This function formats added date
    @detailed
    This function formats added date using user language and default added date
    """
    date = lang.months[real_time.month - 1] + real_time.strftime(" %d, %Y, %H:%M")
    return date


@login_required
def get_note_data(request):
    """
    @brief
    This function receives information about notes
    @detailed
    This function receives information about notes such as date, time, name
    """
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        lang, language = get_language(request)
        note_id = request.POST.get('id')
        response_data = dict()
        result = 100
        if note_id:
            notes = Notes.objects.filter(user=request.user, id=note_id)
            if len(notes) > 0:
                note = notes[0]
                response_data = {
                    'title': note.title,
                    'data': note.data,
                    'added_time': create_added_date(lang, note.added_time),
                    'id': note.id,
                }
                result = 100
            else:
                result = 111
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def delete_note(request):
    """
    @brief
    This function deletes notes
    """
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        note_id = request.POST.get('id')
        should_return_last_note = request.POST.get('should_return_last_note')
        response_data = dict()
        result = 100
        if note_id:
            result = Notes.delete_note(note_id, request.user)
        if should_return_last_note:
            last_notes = Notes.get_notes("date_up", request.user)
            last_note = None
            if last_notes:
                if last_notes.count() >= 3:
                    last_note = last_notes[0:3][-1]
            if last_note is not None:
                response_data['id'] = last_note.id
                response_data['title'] = last_note.title
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def search(request, sorting_type="date_up"):
    """
    @brief
    This function looks for the notes
    @detailed
    This function searches for a note among those that exist
    """
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        aim = request.POST.get('aim')
        if aim is None:
            aim = ""
        found_notes = Notes.search_notes(aim, request.user, sorting_type)
        json_serializable_notes = [{'id': note.id, 'title': note.title} for note in found_notes]
        response = {
            'found_notes': json_serializable_notes
        }
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def sort_notes(request):
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        sorting_type = request.POST.get('sorting_type')
        response = search(request, sorting_type)
        return response
