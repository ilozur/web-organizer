from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.forms import *
from notes.models import Notes
import json


@login_required
def index(request):
    context = {
        'title': "Notes index page",
        'header': "Notes index page header",
    }
    notes_list = list()
    user = request.user
    notes = Notes.get_notes('title_up', user)
    for i in notes:
        notes_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id, [i.data]))
    context['notes_data'] = notes_list
    search_form = SearchForm()
    context['search_form'] = search_form
    form = AddNoteForm()
    context['add_form'] = form
    form = ShowNoteForm()
    context['show_form'] = form
    return render(request, "notes/index.html", context)


@login_required
def add_note_ajax(request):
    response_data = {}
    if request.method == "POST":
        form = AddNoteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['title']
            data = form.cleaned_data['data']
            tmp = Notes(name=name, data=data, user=request.user)
            tmp.save()
            result = "Success"
            response_data['id'] = tmp.id
        else:
            result = 'form not valid'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def search_notes(substr, user):
    obj = Notes.get_notes('all', user)
    ret_list = list()
    for i in obj:
        if substr in i.name:
            ret_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id, [i.data]))
    return ret_list


@login_required
def show_note(request, id):
    context = {}
    if request.POST:
        note = Notes.get_note_by_id(id)
        note.data = request.POST['data']
        note.save()
        return HttpResponseRedirect('/notes')
    else:
        if Notes.get_note_by_id(id) is not None:
            note = Notes.get_note_by_id(id)
            context = {
                'header': "Show note page header",
                'id': id,
                'title': note.name
            }
            form = ShowNoteForm({'data': note.data})
            context['form'] = form
        else:
            context['error'] = True
        return render(request, "notes/show_note.html", context)


@login_required
def search_ajax(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            form = SearchForm(request.POST)
            if form.is_valid():
                string = form.data['result']
                response_data = {
                    'notes_list': search_notes(string, request.user)
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
        if request.user.is_authenticated:
            print(request.POST)
            request.POST.get('id')
            id = request.POST.get('id')
            name = request.POST.get('title')
            data = request.POST.get('data')
            if Notes.objects.filter(id=id).first():
                tmp = Notes.objects.filter(id=id).first()
                tmp.name = name
                tmp.data = data
                tmp.save()
                result = 'Success'
            else:
                result = 'No such note'
        else:
            result = 'user is not authenticated'
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
                result = "Success"
            else:
                result = "Sorry, Note does not exist"
        else:
            result = 'user is not authenticated'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')
