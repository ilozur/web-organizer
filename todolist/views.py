from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
import os

from todolist import models
from todolist.forms import AddTodoForm
from todolist.models import Todos
from django import forms
import datetime
import json



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
    context = {'user': request.user}
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
    context = {
        'title': "Completed todos page",
        'header': "You can mark available todos as uncompleted"
    }
    items = Todos.objects.filter(status='done')
    if request.GET:
        sorting(request.GET, items)
    if request.POST:
        change_status(request.POST, items)
    return render(request, "todolist/done_todos.html", {'items': items}, context)


def sorting(type, items):
    type = list(type)
    mode = {
        'AtoZ': items.order_by('title'),
        'ZtoA': (items.order_by('title')).reverse(),
        'old': items.order_by('added_date', 'added_time'),
        'new': (items.order_by('added_date', 'added_time')).reverse()
    }
    return mode.get(type[0], items.all())


def change_status(data, items):
    title = list(data.keys())
    mode = {
        'Reopen': 'in progress',
        'Done': 'done'
    }
    title.remove('csrfmiddlewaretoken')
    obj = items.get(title=title[0])
    obj.status = mode.get(data.get(title[0]))
    obj.save()


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
def save_todo(request,id):
    context = {}
    context['user'] = request.user
    saving_todo = Todos.objects.get(id=id).first()
    f = open('saved_todos/todo.txt', 'wt')
    f.write(saving_todo.title)
    f.write(saving_todo.text)
    f.close()
    context['title'] = saving_todo.title
    return render(request, 'saving.html', context)


@csrf_exempt
def sort_ajax(request):
    if request.method == "POST":
        todo_list = list()
        sort_type = request.POST.get('data')
        for i in Todos.get_todos(sort_type):
            todo_list.append((i.title, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.text))
        response = {'todo_list': todo_list}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponseRedirect('/')