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
import time


def index(request):
    context = {
        'title': "Todolist index page",
        'header': "Todolist index page header"
    }
    return render(request, "todolist/index.html", context)


@login_required
def add_todo(request):
    context = {}
    context['user'] = request.user
    if request.POST:
        form = AddTodoForm(request.POST)
        if form.is_valid():
            user = request.user
            time_for_todo()
            date_for_todo()
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


def time_for_todo():
    timer = tuple()
    timer.asctime()
    todo_time = []
    spaces = 0
    for i in range(len(timer)):
        if timer[i] == ' ':
            spaces += 1
        if spaces == 2:
            todo_time.append(timer[i])
    return todo_time


def date_for_todo():
    date = tuple()
    date.asctime()
    todo_date = []
    spaces = 0
    for i in range(len(date)):
        if date[i] == ' ':
            spaces += 1
        if (spaces > 2) or (spaces < 2):
            todo_date.append(date[i])
    return todo_date


def Read_file(file_name):
    s = open(file_name, "r")
    a = s.split(" ")
    user = a[0]
    if a[1] == None:
        added_time = time_for_todo()
    else:
        added_time = a[1]
    if a[2] == None:
        added_date = time_for_todo()
    else:
        added_date = a[2]
    priority = a[3]
    status = a[4]
    deadline = a[5]
    text = a[6]
    title = a[7]
    p = Todos(text=text, user=user, title=title, added_time=added_time,
              added_date=added_date, priority=priority, deadline=status)
    p.save()
