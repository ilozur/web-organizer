from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from notes.forms import *
from main.models import Language
import json
from datetime import datetime
from notes.forms import AddNoteForm, SearchForm
from notes.models import Notes
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from localisation import eng, rus


@login_required
def index(request):
    sort_type = request.GET.get("sort_type", "date_up")
    notes = Notes.get_notes(sort_type, user=request.user)
    page = request.GET.get("page")
    try:
        page = int(page)
    except Exception as ex:
        page = 1
        print(ex)
    if request.method == "GET":
        context = {
            'title': "Notes index page",
        }
        user_lang = Language.objects.filter(user=request.user).first().lang
        if user_lang == "ru":
            lang = rus
        elif user_lang == "en":
            lang = eng
        else:
            lang = eng
        context['language'] = user_lang
        context['lang'] = lang
        notes_list = []
        for i in notes:
            notes_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id, i.data_part))
        pages = Paginator(notes_list, 20)
        if (page < 1) or (page > len(pages.page_range)):
            page = 1
        context['page'] = page
        context['all_notes_count'] = notes.count()
        context['voice_notes_count'] = notes.filter(is_voice=True).count()
        context['text_notes_count'] = int(context['all_notes_count']) - int(context['voice_notes_count'])
        context['notes_data'] = pages.page(page)
        context['back_paginate_btn'] = pages.page(page).has_previous()
        context['next_paginate_btn'] = pages.page(page).has_next()
        context['notes_pages'] = pages.page_range
        context['search_note_form'] = SearchForm()
        context['add_note_form'] = AddNoteForm()
        context['edit_note_form'] = EditNoteForm()
        return render(request, "notes/index.html", context)
    else:
        response = paginate(notes, page)
        return response


@login_required
def add_note_ajax(request):
    """
    @brief
    This function adds notes
    """
    response_data = {}
    if request.method == "POST":
        form = AddNoteForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['note_title']
            data = form.cleaned_data['note_data']
            data_part = form.cleaned_data['note_data_part']
            tmp = Notes(name=name, data=data, added_time=datetime.now(), user=request.user, data_part=data_part)
            tmp.save()
            result = "100"
            response_data['data_part'] = tmp.data_part
            response_data['id'] = tmp.id
            response_data['name'] = tmp.name
            response_data['datetime'] = datetime.now().strftime("%I:%M%p on %B %d, %Y")
        else:
            result = '104'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def search_notes(substr, user):
    obj = Notes.objects.all()
    ret_list = []
    """
        @brief
        This function searches notes
        """
    for i in obj:
        if substr in i.name:
            ret_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id, [i.data]))
    return ret_list


@login_required
def get_note_data_ajax(request):
    """
    @brief
    This function receives information about notes
    @detailed
    This function receives information about notes such as date, time, name
    """
    response_data = {}
    if request.method == "POST":
        note_id = request.POST.get('id')
        if Notes.objects.filter(user=request.user, id=note_id).count() > 0:
            note = Notes.objects.filter(id=note_id).first()
            response_data = {
                'title': note.name,
                'data': note.data,
                'added_time': note.added_time.strftime("%I:%M%p on %B %d, %Y"),
            }
            if note.last_edit_time is not None:
                response_data['last_edit_time'] = note.last_edit_time.strftime("%I:%M%p on %B %d, %Y")
            result = '100'
        else:
            result = '111'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def search_ajax(request):
    """
    @brief
    This function looks for the notes
    @detailed
    This function searches for a note among those that exist
    """
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            string = form.data['result']
            response_data = {
                'notes_list': Notes.search_notes(string, request.user)
            }
            result = '100'
        else:
            response_data = {
                'notes_list': Notes.get_notes(request.sorting_type, request.user)
            }
            result = '104'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')

@login_required
def save_ajax(request):
    """
    @brief
    This function saves the notes
    @detailed
    This function saves the written note
    """
    response_data = {}
    if request.method == "POST":
        form = EditNoteForm(request.POST)
        if form.is_valid():
            note_id = form.cleaned_data['note_id']
            if Notes.objects.filter(user=request.user, id=note_id).count() > 0:
                tmp = Notes.objects.filter(id=note_id).first()
                tmp.name = form.cleaned_data['note_title_edit']
                tmp.data = form.cleaned_data['note_data_edit']
                tmp.data_part = form.cleaned_data['note_data_part_edit']
                tmp.last_edit_time = datetime.now()
                tmp.save()
                result = '100'
                response_data['edited_time'] = datetime.now().strftime("%I:%M%p on %B %d, %Y")
                response_data['data_part'] = tmp.data_part
            else:
                result = '111'
        else:
            result = '104'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def delete_ajax(request):
    """
    @brief
    This function deletes notes
    """
    response_data = {}
    if request.method == "POST":
        note_id = request.POST.get('id')
        should_return_last_note = request.POST.get('return_last_note')
        if Notes.objects.filter(user=request.user, id=note_id).count() > 0:
            if Notes.delete_note(note_id):
                result = "100"
            else:
                result = "111"
        else:
            result = "111"
        last_notes = Notes.get_notes("date_up", request.user)
        last_note = None
        if last_notes:
            if last_notes.count() >= 3:
                last_note = last_notes[0:3][-1]
        if (last_note is not None) and should_return_last_note:
            response_data['id'] = last_note.id
            response_data['name'] = last_note.name
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def paginate(notes, page_number):
    response_data = {}
    notes_list = []
    for i in notes:
        notes_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id, i.data_part))
    pages = Paginator(notes_list, 20)
    if (page_number < 1) or (page_number > len(pages.page_range)):
        page_number = 1
    response_data['buttons'] = [pages.page(page_number).has_previous(), pages.page(page_number).has_next()]
    response_data['notes_list'] = pages.page(page_number).object_list
    response_data['result'] = 100
    response_data['normal_page'] = page_number
    return HttpResponse(json.dumps(response_data), content_type="application/json")
