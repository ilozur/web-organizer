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
    items = Todos.objects.filter(status='in progress')
    items = Todos.objects.order_by('title')
    if (request.GET.get('ZtoA')):
        items = reversed(Todos.objects.order_by('title'))
    elif (request.GET.get('old')):
        items = Todos.objects.order_by('added_date', 'added_time')
    elif (request.GET.get('new')):
        items = reversed(Todos.objects.order_by('added_date', 'added_time'))
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
    addtime = datetime.datetime.now()
    print(addtime)
    addtime = addtime.strftime("%H:%M:%S %Y-%m-%d")
    print(addtime)
    dater, timer = addtime.split(' ')
    return timer, dater


def completed_todos(request):
    items = Todos.objects.filter(status='done')
    context = {
        'title': "Completed todos page",
        'header': "You can mark avaliable todos as uncompleted"
    }
    return render(request, "todolist/done_todos.html", {'items': items}, context)

