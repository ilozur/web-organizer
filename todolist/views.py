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
    return render(request, "todolist/index.html", context)


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
        'title': "Completed todos page",
        'header': "You can mark available todos as uncompleted"
    }
    todo_list = Todos.get_todos('AtoZ', 'done', request.user)
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
def save_todo(request,id):
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


@csrf_exempt
def view(request):
    response = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            captions = {
                'done': ['in progress','Reopen', 'Todos'],
                'in progress': ['done', 'Done', 'Done Todos']
            }
            status = request.POST.get('status')
            print(captions.get(status)[0])
            response['todo_list'] = Todos.get_todos('AtoZ', status, request.user)
            response['captions'] = captions.get(status)
            response['result'] = "Success"
        else:
            response['result'] = "User is not authenticated"
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseRedirect('/')