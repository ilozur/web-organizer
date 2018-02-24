from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
import os
from todolist.forms import AddTodoForm
from todolist.models import Todos
from django import forms
import datetime
sortTodo_list = []
timeTodo_list = []


def index(request):
    items = checkType_of_sort(type_of_sort='default')
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
    items = checkType_of_sort(type_of_sort='default')
    for item in items:
        if item.status == 'in progress':
            items.pop(item)
    context = {
        'title': "Completed todos page",
        'header': "You can mark avaliable todos as uncompleted"
    }
    return render(request, "todolist/done_todos.html", context, {'items': items})


def checkType_of_sort(type_of_sort):
    if type_of_sort == 'old':
        return timeTodo_list
    elif type_of_sort == 'new':
        reversed = timeTodo_list
        reversed.reverse()
        return reversed
    elif type_of_sort == 'default':
        return Todos.objects.all()
    elif type_of_sort == 'A to Z':  # Мишина сортировка
        return sortTodo_list       #
    elif type_of_sort == 'Z to A':  #
        return sortTodo_list
