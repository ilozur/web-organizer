from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
import os
from todolist.forms import AddTodoForm
from todolist.models import Todos
from django import forms
import time


def index(request):
    items = Todos.objects.all()
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
                time_for_todo()
                date_for_todo()
                p = Todos(text=form.data['text'], user=user, title=form.data['title'], added_time=time_for_todo(),
                          added_date=date_for_todo(), priority=form.data['priority'], deadline=form.data['deadline'])
                p.save()
                context['id'] = p.id
            else:
                context['errors'] = form.errors
            return render(request, 'todolist/add.html', context)
        else:
            form = AddTodoForm()
            context['add_form'] = form
            return render(request, 'todolist/add.html', context)


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
            if (spaces>2) or (spaces<2):
                todo_date.append(date[i])
    return todo_date