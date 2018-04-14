from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from todo.forms import AddTodoForm
from todo.forms import SearchForm
from todo.forms import EditTodoForm
from todo.models import Todos
import json
from datetime import datetime


@login_required
def index(request):
    context = {
        'title': "Todos index page",
        'header': "Todos index page header",
    }
    user = request.user
    todo_list = []
    todos = Todos.get_todos('AtoZ', 'in progress', user)
    for i in todos:
        todo_list.append((i.title, i.added_date_and_time.strftime("%I:%M%p on %B %d, %Y"), i.id))
    context['todo_data'] = todo_list
    context['search_todo_form'] = SearchForm()
    context['add_todo_form'] = AddTodoForm()
    context['edit_todo_form'] = EditTodoForm()
    return render(request, "todo/index.html", context)


@login_required
def add_todo(request):
    response_data = {}
    if request.method == "POST":
        form = AddTodoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            tmp = Todos(title=title, text=text, added_date_and_time=datetime.now(), user=request.user,
                        priority=3)
            tmp.save()
            result = "Success"
            response_data['id'] = tmp.id
            response_data['title'] = tmp.title
            response_data['datetime'] = datetime.now().strftime("%I:%M%p on %B %d, %Y")
        else:
            result = 'form not valid'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def show_todo(request):
    if request.method == "POST":
        response_data = {}
        todo_id = request.POST.get('id')
        if Todos.get_todo_by_id(todo_id):
            todo = Todos.get_todo_by_id(todo_id)
            response_data = {'title': todo.title, 'text': todo.text,
                             'added_date_and_time': todo.added_date_and_time.strftime("%I:%M%p on %B %d, %Y"),
                             'result': "Success"
                             }
        else:
            response_data['result'] = "Todo does not exist"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def sorting(request):
    response = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            sort_type = request.POST.get('data')
            todo_list = Todos.get_todos(sort_type, 'in progress', request.user)
            response = {
                'todo_list': todo_list,
                'result': "Success"
            }
        else:
            response['result'] = "User is not authenticated"
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def status_change(request):
    response = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            todo_id = request.POST.get('id')
            todo_type = request.POST.get('type')
            obj = Todos.get_todo_by_id(todo_id)
            obj.status = todo_type
            obj.save()
            response['result'] = "Success"
        else:
            response['result'] = "User is not authenticated"
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseRedirect('/')


@login_required
def edit_todo(request):
    response_data = {}
    if request.method == "POST":
        form = EditTodoForm(request.POST)
        if form.is_valid():
            todo_id = form.cleaned_data['note_id']
            if Todos.get_todo_by_id(id=todo_id).count() > 0:
                tmp = Todos.get_todo_by_id(id=todo_id).first()
                tmp.title = form.cleaned_data['todo_title_edit']
                tmp.text = form.cleaned_data['todo_text_edit']
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
def read_file(file_name):
    s = open(file_name, "r")
    s = s.read()
    a = s.split("\n")
    user = a[0]
    date, time = '00-00-00', '34'
    if not (a[1]):
        added_time = time
    else:
        added_time = a[1]
    if not (a[2]):
        added_date = date
    else:
        added_date = a[2]
    priority = a[3]
    if not (a[4]):
        status = "in progress"
    else:
        status = a[4]
    deadline = a[5]
    text = a[6]
    title = a[7]
    p = Todos(text=text, user=user, title=title, added_time=added_time,
              added_date=added_date, priority=priority, deadline=deadline, status=status)
    p.save()


@login_required
def delete_todo(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            id = request.POST.get('id')
            if Todos.delete_todo(id):
                result = "success"
            else:
                result = "Sorry, Todo does not exist"
        else:
            result = 'user is not authenticated'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def search(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            form = SearchForm(request.POST)
            if form.is_valid():
                string = form.data['result']
                response_data = {
                    'todo_list': Todos.search_todos(string, request.user)
                }
                result = 'Success'
            else:
                response_data = {
                    'todo_list': Todos.get_todos(request.sorting_type, 'in progress', request.user)
                }
                result = 'Form is not valid'
        else:
            result = 'user is not authenticated'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')
