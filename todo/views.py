from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import os
from todo.forms import AddTodoForm
from todo.forms import ShowTodoForm
from todo.models import Todos
from django import forms
import json


@login_required
def index(request):
    context = {
        'title': "Todos index page",
        'header': "Todos index page header",
    }
    user = request.user
    todo_list = Todos.get_todos('AtoZ', 'in progress', user)
    context['items'] = todo_list
    return render(request, "todo/index.html", context)


@login_required
def add_todo(request):
    context = {'user': request.user}
    if request.POST:
        form = AddTodoForm(request.POST)
        if form.is_valid():
            user = request.user
            p = Todos(text=form.data['text'], user=user, title=form.data['title'],
                      priority=form.data['priority'], deadline=form.data['deadline'])
            p.save()
            context['id'] = p.id
        else:
            context['errors'] = form.errors
        return render(request, 'todolist/add.html', context)
    else:
        form = AddTodoForm()
        context['add_form'] = form
        return render(request, 'todolist/add.html', context)


@login_required
def completed_todos(request):
    context = {
        'title': "Todos index page",
        'header': "Todos index page header",
    }
    user = request.user
    todo_list = Todos.get_todos('AtoZ', 'done', user)
    context['items'] = todo_list
    return render(request, "todolist/done_todos.html", context)


@login_required
def show_todo(request, id):
    context = {'user': request.user}
    todo_now = Todos.objects.get(id=id).first()
    if todo_now is None:
        context['errors'] = ['NOT FOUND']
    else:
        context['a'] = todo_now
        return render(request, 'show.html', context)


@login_required
def save_todo(request, id):
    context = {'user': request.user}
    saving_todo = Todos.objects.get(id=id).first()
    f = open('saved_todos/todo.txt', 'wt')
    f.write(saving_todo.title)
    f.write(saving_todo.text)
    f.close()
    context['title'] = saving_todo.title
    return render(request, 'saving.html', context)


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
            id = request.POST.get('id')
            type = request.POST.get('type')
            obj = Todos.get_todo_by_id(id)
            obj.status = type
            obj.save()
            response['result'] = "Success"
        else:
            response['result'] = "User is not authenticated"
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseRedirect('/')


@login_required
def show_todolist(request):
    context = {}
    if request.POST:
        form = ShowTodoForm(request)
        Todo = Todos.get_todo_by_id(id)
        Todolist = request.POST
        Todolist.data = request.POST['data']
        Todolist.text = request.POST['text']
        Todolist.save()
        return HttpResponseRedirect('/todolist')
    return render(request, "todolist/index.html", context)


@login_required
def edit_todolist(request, id):
    context = {}
    if request.POST:
        form = ShowTodoForm(request)
        Todo = Todos.objects.filter(id=id).first()
        Todo.data = request.POST['data']
        Todo.data = request.POST['text']
        Todo.save()
        return HttpResponseRedirect('/todolist')
    else:
        if len(Todos.objects.filter(id=id)) > 0:
            todo = Todos.objects.filter(id=id).first()
            context = {
                'header': "Show todo page header",
                'id': id,
                'title': todo.title,
                'priority': todo.priority
            }
            form = ShowTodoForm({'text': todo.text})
            context['form'] = form
        else:
            context['error'] = True
        return render(request, "todolist/show.html", context)


@login_required
def Read_file(file_name):
    s = open(file_name, "r")
    s = s.read()
    a = s.split("\n")
    user = a[0]
    date, time = time_and_date_for_todo()
    if not(a[1]):
        added_time = time
    else:
        added_time = a[1]
    if not(a[2]):
        added_date = date
    else:
        added_date = a[2]
    priority = a[3]
    if not(a[4]):
        status = "in progress"
    else:
        status = a[4]
    deadline = a[5]
    text = a[6]
    title = a[7]
    p = Todos(text=text, user=user, title=title, added_time=added_time,
              added_date=added_date, priority=priority, deadline=deadline, status=status)
    p.save()
