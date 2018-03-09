from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
import os

from todolist import models
from todolist.forms import AddTodoForm
from todolist.models import Todos
from django import forms
import datetime

def index(request):
    for item in items:
        if not (item.status == 'in progress'):
            items.pop(item)
    context = {
        'title': "Todolist index page",
        'header': "Todolist index page header"
    }
    return render(request, "todolist/index.html", context, {'items': items})


#@login_required
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
                global timeTodo_list
                timeTodo_list.append(p)
                context['id'] = p.id
            else:
                context['errors'] = form.errors
            return render(request, 'todolist/add.html', context)
        else:
            form = AddTodoForm()
            context['add_form'] = form
            return render(request, 'todolist/add.html', context)


def time_and_date_for_todo():
    addtime = datetime.datetime.now()
    addtime = addtime.strftime("%d-%m-%Y %H:%M")
    dater, timer = addtime.split(' ')
    return timer, dater


def completed_todos(request):
    for item in items:
        if item.status == 'in progress':
            items.pop(item)
    context = {
        'title': "Completed todos page",
        'header': "You can mark avaliable todos as uncompleted"
    }
    return render(request, "todolist/done_todos.html", context, {'items': items})


@login_required
def add_todo(request):
    context = {}
    context['user'] = request.user
    if request.POST:
        form = AddTodoForm(request.POST)
        if form.is_valid():
            user = request.user
            p = Todos(text=form.data['text'], user=user, title=form.data['title'], added_time=time_for_todo(),
                      added_date=date_for_todo(), priority=form.data['priority'], deadline=form.data['deadline'])
            p.save()
            context['id'] = p.id
        else:
            context['errors'] = form.errors
        return render(request, 'add_result.html', context)
    else:
        form = AddTodoForm()
        context['add_form'] = form
        return render(request, 'add.html', context)


def show_todo(request, id):
    context = {}
    context['user'] = request.user
    todo_now = Todos.objects.get(id=id).first()
    if todo_now is None:
        context['errors'] = ['NOT FOUND']
    else:
        context['a'] = todo_now
        return render(request, 'show.html', context)



def Read_file(file_name):
    s = open(file_name, "r")
    s = s.read()
    a = s.split("\n")
    user = a[0]
    if a[1] == None:
        added_time = time_for_todo()
    else:
        added_time = a[1]
    if a[2] == None:
        added_date = date_for_todo()
    else:
        added_date = a[2]
    priority = a[3]
    if a[4] == None:
        status = "in progress"
    else:
        status = a[4]
    deadline = a[5]
    text = a[6]
    title = a[7]
    p = Todos(text=text, user=user, title=title, added_time=added_time,
              added_date=added_date, priority=priority, deadline=deadline, status=status)
    p.save()
