from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
import re

from todo.forms import *
from todo.models import *
from main.models import Timezone
import pytz

from main.views import get_language


@login_required
def index(request):
    if request.method == "GET":
        todos = Todos.get_todos("date_up", request.user)
        context = dict()
        context['title'] = "Todos index page"
        context['lang'], context['language'] = get_language(request)
        folders = TodosFolder.objects.filter(user=request.user, done=False)
        done_folder = TodosFolder.objects.filter(user=request.user, done=True)
        if len(done_folder) == 0:
            tmp_folder = TodosFolder(user=request.user, title="Recently deleted", done=True)
            tmp_folder.save()
        done_folder = TodosFolder.objects.filter(user=request.user, done=True)
        context['done_folder'] = done_folder[0]
        context['all_folder'] = {'id': 'all'}
        context['folders'] = folders
        if len(todos) > 0:
            context['todos'] = todos
            context['no_todos'] = False
        else:
            context['no_todos'] = True
        context['save_todo_form'] = SaveTodoForm()
        return render(request, "todo/index.html", context)


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
def get_todo_data(request):
    """
    @brief
    This function receives information about todos
    @detailed
    This function receives information about todos such as date, time, name
    """
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        lang, language = get_language(request)
        todo_id = request.POST.get('id')
        response = dict()
        result = 100
        if todo_id:
            todos = Todos.objects.filter(user=request.user, id=todo_id)
            if len(todos) > 0:
                todo = todos[0]
                tzinfo = pytz.timezone(Timezone.objects.filter(user=request.user)[0].timezone)
                response = {
                    'title': todo.title,
                    'data': todo.data,
                    'added_time': create_added_date(lang, todo.added_time.astimezone(tzinfo)),
                    'id': todo.id,
                }
                result = 100
            else:
                result = 111
        response['result'] = result
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_todo(request):
    """
    @brief
    This function deletes todos
    """
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        todo_id = request.POST.get('id')
        should_return_last_todo = request.POST.get('should_return_last_todo')
        response = dict()
        result = 100
        if todo_id:
            result = Todos.delete_todo(todo_id, request.user)
        if should_return_last_todo:
            last_todos = Todos.get_todos("date_up", request.user)
            last_todo = None
            if last_todos:
                if last_todos.count() >= 3:
                    last_todo = last_todos[0:3][-1]
            if last_todo is not None:
                response['id'] = last_todo.id
                response['title'] = last_todo.title
        response['result'] = result
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def search(request):
    """
    @brief
    This function looks for the todos
    @detailed
    This function searches for a todo among those that exist
    """
    sorting_type = request.POST.get('sorting_type')
    aim = request.POST.get('aim')
    folder_id = request.POST.get('folder')
    if folder_id == "all":
        folder_id = None
    if folder_id:
        folder = TodosFolder.objects.filter(id=folder_id)
        if len(folder) == 0:
            folder = None
        else:
            folder = folder[0]
    else:
        folder = None
    found_todos = Todos.search_todos(aim, request.user, sorting_type, folder)
    json_serializable_todos = [{'id': todo.id, 'title': todo.title} for todo in found_todos]
    response = {
        'found_todos': json_serializable_todos
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
            folder = TodosFolder.objects.filter(id=folder_id)
            if len(folder) == 0:
                folder = None
            else:
                folder = folder[0]
        else:
            folder = None
        sorted_todos = Todos.search_todos(aim, request.user, sorting_type, folder)
        json_serializable_todos = [{'id': todo.id, 'title': todo.title} for todo in sorted_todos]
        response = {
            'sorted_todos': json_serializable_todos
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
            todos = Todos.get_todos(sorting_type, user=request.user)
            json_serializable_todos = [{'id': todo.id, 'title': todo.title} for todo in todos]
            response['todos'] = json_serializable_todos
            result = "100"
        else:
            folder = TodosFolder.objects.filter(id=folder_id)
            if len(folder) == 0:
                result = "115"
            else:
                folder = folder[0]
                todos = Todos.get_todos(sorting_type, user=request.user, folder=folder)
                json_serializable_todos = [{'id': todo.id, 'title': todo.title} for todo in todos]
                response['todos'] = json_serializable_todos
                result = "100"
        response['result'] = result
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def save_todo(request):
    if request.method == "GET":
        return HttpResponseRedirect('/')
    else:
        todo_id = request.POST.get('id')
        form_save = SaveTodoForm(request.POST)
        form_edit = EditTodoForm(request.POST)
        if form_save.is_valid():
            form = form_save
            title_key = "todo_title"
            data_key = "todo_data"
        else:
            form = form_edit
            title_key = "todo_title_edit"
            data_key = "todo_data_edit"
        result = "100"
        response = dict()
        if form.is_valid():
            if todo_id == "new_todo":
                folder = request.POST.get('folder')
                if folder == "null":
                    folder = None
                if folder is not None:
                    folder = TodosFolder.objects.filter(id=folder)[0]
                if form.cleaned_data[title_key] == "":
                    tmp_title = re.sub('<[^>]*>', '', form.cleaned_data[data_key])
                    tmp_title = tmp_title[0:30]
                    form.cleaned_data[title_key] = tmp_title
                response['id'], response['title'] = add_todo(request.user, form.cleaned_data[title_key],
                                                             form.cleaned_data[data_key], folder)
            else:
                todos = Todos.objects.filter(id=todo_id)
                if len(todos) > 0:
                    todo = todos[0]
                    todo.title = form.cleaned_data[title_key]
                    todo.data = form.cleaned_data[data_key]
                    todo.save()
                    response['id'] = todo.id
                else:
                    result = "111"
        else:
            result = "104"
        response['result'] = result
        return HttpResponse(json.dumps(response), content_type="application/json")


def add_todo(user, title, data, folder):
    todo = Todos(title=title, user=user, data=data, folder=folder)
    todo.save()
    return todo.id, todo.title
