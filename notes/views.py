from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json

from notes.forms import *
from notes.models import *

from datetime import datetime
from django.utils import timezone
import pytz

from main.views import get_language


@login_required
def index(request):
    if request.method == "GET":
        notes = Notes.get_notes("date_up", request.user)
        context = dict()
        context['title'] = "Notes index page"
        context['lang'], context['language'] = get_language(request)
        folders = NotesFolder.objects.filter(user=request.user, recently_deleted=False)
        recently_deleted_folder = NotesFolder.objects.filter(user=request.user, recently_deleted=True)
        if len(recently_deleted_folder) == 0:
            tmp_folder = NotesFolder(user=request.user, title="Recently deleted", recently_deleted=True)
            tmp_folder.save()
        recently_deleted_folder = NotesFolder.objects.filter(user=request.user, recently_deleted=True)
        context['recently_deleted_folder'] = recently_deleted_folder[0]
        context['all_folder'] = {'id': 'all'}
        context['folders'] = folders
        if len(notes) > 0:
            context['notes'] = notes
            context['no_notes'] = False
        else:
            context['no_notes'] = True
        context['save_note_form'] = SaveNoteForm()
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
        response = dict()
        result = 100
        if note_id:
            notes = Notes.objects.filter(user=request.user, id=note_id)
            if len(notes) > 0:
                note = notes[0]
                response = {
                    'title': note.title,
                    'data': note.data,
                    'added_time': create_added_date(lang, note.added_time),
                    'id': note.id,
                }
                result = 100
            else:
                result = 111
        response['result'] = result
        return HttpResponse(json.dumps(response), content_type="application/json")


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
        response = dict()
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
                response['id'] = last_note.id
                response['title'] = last_note.title
        response['result'] = result
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def search(request):
    """
    @brief
    This function looks for the notes
    @detailed
    This function searches for a note among those that exist
    """
    sorting_type = request.POST.get('sorting_type')
    aim = request.POST.get('aim')
    folder_id = request.POST.get('folder')
    if folder_id == "all":
        folder_id = None
    if folder_id:
        folder = NotesFolder.objects.filter(id=folder_id)
        if len(folder) == 0:
            folder = None
        else:
            folder = folder[0]
    else:
        folder = None
    found_notes = Notes.search_notes(aim, request.user, sorting_type, folder)
    json_serializable_notes = [{'id': note.id, 'title': note.title} for note in found_notes]
    response = {
        'found_notes': json_serializable_notes
    }
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def sort(request):
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        sorting_type = request.POST.get('sorting_type')
        aim = request.POST.get('aim')
        folder_id = request.POST.get('folder')
        if folder_id == "all":
            folder_id = None
        if folder_id:
            folder = NotesFolder.objects.filter(id=folder_id)
            if len(folder) == 0:
                folder = None
            else:
                folder = folder[0]
        else:
            folder = None
        sorted_notes = Notes.search_notes(aim, request.user, sorting_type, folder)
        json_serializable_notes = [{'id': note.id, 'title': note.title} for note in sorted_notes]
        response = {
            'sorted_notes': json_serializable_notes
        }
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def get_folder(request):
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        folder_id = request.POST.get('id')
        sorting_type = request.POST.get('sorting_type')
        if sorting_type is None:
            sorting_type = "date_up"
        response = dict()
        if folder_id == "all":
            notes = Notes.get_notes(sorting_type, user=request.user)
            json_serializable_notes = [{'id': note.id, 'title': note.title} for note in notes]
            response['notes'] = json_serializable_notes
            result = "100"
        else:
            folder = NotesFolder.objects.filter(id=folder_id)
            if len(folder) == 0:
                result = "115"
            else:
                folder = folder[0]
                notes = Notes.get_notes(sorting_type, user=request.user, folder=folder)
                json_serializable_notes = [{'id': note.id, 'title': note.title} for note in notes]
                response['notes'] = json_serializable_notes
                result = "100"
        response['result'] = result
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def save_note(request):
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        note_id = request.POST.get('id')
        form_save = SaveNoteForm(request.POST)
        form_edit = EditNoteForm(request.POST)
        if form_save.is_valid():
            form = form_save
            title_key = "note_title"
            data_key = "note_data"
        else:
            form = form_edit
            title_key = "note_title_edit"
            data_key = "note_data_edit"
        result = "100"
        response = dict()
        if form.is_valid():
            if note_id == "new_note":
                folder = request.POST.get('folder')
                if folder == "null":
                    folder = None
                if folder is not None:
                    folder = NotesFolder.objects.filter(id=folder)[0]
                response['id'] = add_note(request.user, form.cleaned_data[title_key],
                                          form.cleaned_data[data_key], folder)
            else:
                notes = Notes.objects.filter(id=note_id)
                if len(notes) > 0:
                    note = notes[0]
                    note.title = form.cleaned_data[title_key]
                    note.data = form.cleaned_data[data_key]
                    note.save()
                    response['id'] = note.id
                else:
                    result = "111"
        else:
            result = "104"
        response['result'] = result
        return HttpResponse(json.dumps(response), content_type="application/json")


def add_note(user, title, data, folder):
    note = Notes(title=title, user=user, data=data, folder=folder)
    note.save()
    return note.id
