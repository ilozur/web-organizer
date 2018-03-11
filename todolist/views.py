from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import json
import os

from todolist import models
from todolist.forms import AddTodoForm
from todolist.models import Todos
from django import forms
import datetime


@login_required
def index(request):
    context = {
        'title': "Todos index page",
        'header': "Todos index page header",
    }
    todo_list = list()
    user = request.user
    todos = Todos.get_todos('AtoZ', user)
    for i in todos:
        todo_list.append((i.title, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id))
    context['todo_data'] = todo_list
    return render(request, "todolist/index.html", context)


@login_required
def add_todo(request):
    context = {}
    context['user'] = request.user
    if request.POST:
        form = AddTodoForm(request.POST)
        if form.is_valid():
            user = request.user
            date, time = time_and_date_for_todo()
            p = Todos(text=form.data['text'], user=user, title=form.data['title'], added_time=time,
                      added_date=date, priority=form.data['priority'], deadline=form.data['deadline'])
            p.save()
            context['id'] = p.id
        else:
            context['errors'] = form.errors
        return render(request, 'todolist/add.html', context)
    else:
        form = AddTodoForm()
        context['add_form'] = form
        return render(request, 'todolist/add.html', context)


def time_and_date_for_todo():
    addtime = (datetime.datetime.now()).strftime("%H:%M:%S %Y-%m-%d")
    dater, timer = addtime.split(' ')
    return timer, dater


@login_required
def completed_todos(request):
    type = list(request.GET.keys())
    items = sorting(type)
    items = items.filter(status='done')
    context = {
        'title': "Completed todos page",
        'header': "You can mark avaliable todos as uncompleted"
    }
    return render(request, "todolist/done_todos.html", {'items': items}, context)


@login_required
def show_todo(request, id):
    context = {}
    context['user'] = request.user
    todo_now = Todos.objects.get(id=id).first()
    if todo_now is None:
        context['errors'] = ['NOT FOUND']
    else:
        context['a'] = todo_now
        return render(request, 'show.html', context)


@login_required
def save_todo(request, id):
    context = {}
    context['user'] = request.user
    saving_todo = Todos.objects.get(id=id).first()
    f = open('saved_todos/todo.txt', 'wt')
    f.write(saving_todo.title)
    f.write(saving_todo.text)
    f.close()
    context['title'] = saving_todo.title
    return render(request, 'saving.html', context)


def sort_ajax(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            sorting_types = ('AtoZ', 'ZtoA', 'old', 'new')
            sort_type = request.POST.get('data')
            if sort_type in sorting_types:
                todo_list = list()
                for i in Todos.get_todos(sort_type, request.user):
                    todo_list.append((i.title, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id))
                response_data = {
                    'todo_list': todo_list
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
