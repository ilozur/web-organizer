from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.forms import *
import json
from datetime import datetime
from notes.forms import AddNoteForm, SearchForm
from notes.models import Notes

@login_required
def index(request):
    context = {
        'title': "Notes index page",
        'header': "Notes index page header",
    }
    user = request.user
    notes_list = []
    context['voice_note'] = Notes.objects.filter(user=request.user, is_voice=True).count()
    context['text_note'] = Notes.objects.filter(user=request.user, is_voice=False).count()
    notes = Notes.get_notes('title_up', user)
    for i in notes:
        notes_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id, [i.data]))
    notes = Notes.get_notes('title_up', user)
    for i in notes:
        notes_list.append((i.name, i.added_time, i.id))
    context['notes_data'] = notes_list
    context['search_note_form'] = SearchForm()
    context['add_note_form'] = AddNoteForm()
    context['edit_note_form'] = EditNoteForm()
    return render(request, "notes/index.html", context)

@login_required
def add_note_ajax(request):
    response_data = {}
    if request.method == "POST":
        form = AddNoteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['note_title']
            data = form.cleaned_data['note_data']
            tmp = Notes(name=name, data=data, added_time=datetime.now(), user=request.user)
            tmp.save()
            result = "Success"
            response_data['id'] = tmp.id
            response_data['name'] = tmp.name
            response_data['datetime'] = datetime.now().strftime("%I:%M%p on %B %d, %Y")
        else:
            result = 'form not valid'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def search(substr):
    obj = Notes.objects.all()
    ret_list = []
    for i in obj:
        if substr in i.name:
            ret_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id, [i.data]))
    return ret_list


@login_required
def get_note_data_ajax(request):
    response_data = {}
    if request.method == "POST":
        note_id = request.POST.get('id')
        if Notes.objects.filter(id=note_id).count() > 0:
            note = Notes.objects.filter(id=note_id).first()
            response_data = {
                'title': note.name,
                'data': note.data,
                'added_time': note.added_time.strftime("%I:%M%p on %B %d, %Y")}
            response_data.append(i)
    return response_data


def show_note(request, id):
    context = {}
    if request.POST:
        note = Notes.objects.filter(id=id).first()
        note.data = request.POST['data']
        note.save()
        return HttpResponseRedirect('/notes')
    else:
        if len(Notes.objects.filter(id=id)) > 0:
            note = Notes.objects.filter(id=id).first()
            response_data = {
                'header': "Show note page header",
                'id': id,
                'title': note.name
            }
            if note.last_edit_time is not None:
                response_data['last_edit_time'] = note.last_edit_time.strftime("%I:%M%p on %B %d, %Y")
            result = 'Success'
        else:
            result = 'Note does not exist'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def search_ajax(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            form = SearchForm(request.POST)
            if form.is_valid():
                string = form.data['result']
                response_data = {
                    'notes_list': Notes.search_notes(string, request.user)
                }
                result = 'Success'
            else:
                response_data = {
                    'notes_list': Notes.get_notes(request.sorting_type, request.user)
                }
                result = 'Form is not valid'
        else:
            result = 'user is not authenticated'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def sort_ajax(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            sorting_types = ('date_up', 'date_down', 'title_up', 'title_down')
            sort_type = request.POST.get('data')
            if sort_type in sorting_types:
                notes_list = list()
                for i in Notes.get_notes(sort_type, request.user):
                    notes_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id, [i.data]))
                response_data = {
                    'notes_list': notes_list
                }
                result = 'Success'
            else:
                result = 'Wrong type'
        else:
            result = 'user is not authenticated'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def save_ajax(request):
    response_data = {}
    if request.method == "POST":
        form = EditNoteForm(request.POST)
        if form.is_valid():
            note_id = form.cleaned_data['note_id']
            if Notes.objects.filter(id=note_id).count() > 0:
                tmp = Notes.objects.filter(id=note_id).first()
                tmp.name = form.cleaned_data['note_title_edit']
                tmp.data = form.cleaned_data['note_data_edit']
                tmp.last_edit_time = datetime.now()
                tmp.save()
                result = 'success'
                response_data['edited_time'] = datetime.now().strftime("%I:%M%p on %B %d, %Y")
            else:
                result = 'No such note'
        else:
            result = 'Form not valid'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def delete_ajax(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            id = request.POST.get('id')
            if Notes.delete_note(id):
                result = "success"
            else:
                result = "Sorry, Note does not exist"
        else:
            result = 'user is not authenticated'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')