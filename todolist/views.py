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
timeTodo_list = []

def index(request):
    typeget = list(request.GET.keys())
    post_data = request.POST
    change_status(post_data)
    items = sorting(typeget)
    items = items.filter(status='in progress')
    context = {
        'title': "Todolist index page",
        'header': "Todolist index page header"
    }
    return render(request, "todolist/index.html", {'items': items}, context)

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
    addtime = (datetime.datetime.now()).strftime("%H:%M:%S %Y-%m-%d")
    dater, timer = addtime.split(' ')
    return timer, dater


def completed_todos(request):
    typeget = list(request.GET.keys())
    post_data = request.POST
    change_status(post_data)
    items = sorting(typeget)
    items = items.filter(status='done')
    context = {
        'title': "Completed todos page",
        'header': "You can mark avaliable todos as uncompleted"
    }
    return render(request, "todolist/done_todos.html", {'items': items}, context)

def sorting(type):
    mode = {
        'AtoZ': Todos.objects.order_by('title'),
        'ZtoA': (Todos.objects.order_by('title')).reverse(),
        'old': Todos.objects.order_by('added_date', 'added_time'),
        'new': (Todos.objects.order_by('added_date', 'added_time')).reverse()
    }
    if type != []:
        return mode.get(type[0], Todos.objects.all())
    else:
        return Todos.objects.all()

def change_status(data):
    title = list(data.keys())
    mode = {
        'Reopen': 'in progress',
        'Done': 'done'
    }
    if title != []:
        title.remove('csrfmiddlewaretoken')
        obj = Todos.objects.get(title=title[0])
        print(data.get(title[0]))
        obj.status = mode.get(data.get(title[0]))
        obj.save()
        print(title)
    else:
        pass