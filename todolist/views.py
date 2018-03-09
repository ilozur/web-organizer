from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
import os

from todolist import models
from todolist.forms import AddTodoForm
from todolist.forms import ShowTodoForm
from todolist.models import Todos
from django import forms
import datetime

def index(request):
    items =Todos
    items = items.filter(status='in progress')
    context = {
        'title': "Todos index page",
        'header': "Todos index page header"
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
                context['id'] = p.id
            else:
                context['errors'] = form.errors
            return render(request, 'todolist/add.html', context)
        else:
            form = AddTodoForm()
            context['add_form'] = form
            return render(request, 'todolist/add.html', context)



def completed_todos(request):
    items = Todos
    items = items.filter(status='done')
    context = {
        'title': "Completed todos page",
        'header': "You can mark avaliable todos as uncompleted"
    }
    return render(request, "todolist/done_todos.html", {'items': items}, context)



def show_todo(request, id):
    context = {}
    context['user'] = request.user
    todo_now = Todos.objects.get(id=id).first()
    if todo_now is None:
        context['errors'] = ['NOT FOUND']
    else:
        context['a'] = todo_now
        return render(request, 'show.html', context)



 def show_todolist(request, id):
    context = {}
    if request.POST:
        form = ShowTodoForm(request)
        Todo = Todos.objects.filter(id=id).first()
        Todolist = request.POST
        Todolist.data = request.POST['data']
        Todolist.save()
        return HttpResponseRedirect('/todolist')
    return render(request, "todolist/index.html", context)
 
 def edit_todolist(request, id):
    context = {}
    if request.POST:
        form = ShowTodoForm(request)
        Todo = Todos.objects.filter(id=id).first()
        Todo.data = request.POST['data']
        Todo.save()
        return redirect('/todolist')
    else:
        if len(Todos.objects.filter(id=id)) > 0:
            todo = Todos.objects.filter(id=id).first()
            context = {
                'header': "Show todo page header",
                'id': id,
                'title': todo.title,
                'priority' : todo.priority
            }
            form = ShowTodoForm({'text': todo.text})
            context['form'] = form
        else:
            context['error'] = True
        return render(request, "todolist/show.html", context)