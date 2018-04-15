from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from main.views import create_mail, send_mail
from todo.forms import AddTodoForm
from todo.forms import SearchForm
from todo.forms import EditTodoForm
from todo.models import Todos
import json
from datetime import datetime


@login_required
def index(request):
    context = {
        'title': "Todos index page",
        'header': "Todos index page header",
    }
    user = request.user
    context['undone_todos'] = Todos.get_todos('AtoZ', 'in progress', user)
    context['done_todos'] = Todos.get_todos('AtoZ', 'done', user)
    context['amount_of_todos'] = Todos.get_amounts(user)
    context['search_todo_form'] = SearchForm()
    context['add_todo_form'] = AddTodoForm()
    context['edit_todo_form'] = EditTodoForm()
    return render(request, "todo/index.html", context)


@login_required
def add_todo(request):
    response_data = {}
    if request.method == "POST":
        form = AddTodoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['todo_title']
            text = form.cleaned_data['todo_text']
            deadline_date = form.cleaned_data['todo_deadline']
            deadline_time = form.cleaned_data['todo_time']
            deadline_date = datetime(deadline_date.year, deadline_date.month, deadline_date.day, deadline_time.hour, deadline_time.minute, 0)
            tmp = Todos(title=title, text=text, added_date_and_time=datetime.now(), user=request.user,
                        priority=form.cleaned_data['todo_priority'], deadline=deadline_date)
            tmp.save()
            result = "Success"
            response_data['id'] = tmp.id
            response_data['title'] = tmp.title
            response_data['datetime'] = datetime.now().strftime("%I:%M%p on %B %d, %Y")
            response_data['priority'] = tmp.priority
        else:
            result = 'form not valid'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def show_todo(request):
    if request.method == "POST":
        todo_id = request.POST.get('id')
        if Todos.objects.filter(id=todo_id).exists():
            todo = Todos.get_todo_by_id(todo_id)
            if todo.status == "in progress":
                current_status = "'done'"
            else:
                current_status = "'in progress'"
            response = {
                'title': todo.title,
                'text': todo.text,
                'added_date_and_time': todo.added_date_and_time.strftime("%I:%M%p on %B %d, %Y"),
                'deadline': todo.deadline.strftime("%I:%M%p on %B %d, %Y"),
                'priority': todo.priority,
                'status': todo.status,
                'time': [todo.deadline.hour, todo.deadline.minute],
                'date': [todo.deadline.year, todo.deadline.month, todo.deadline.day],
                'id': todo.id,
                'result': "Success",
                'current_status': current_status
            }
        else:
            response = {
                'result': "User is not authenticated"
            }
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


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
            todo_id = request.POST.get('id')
            todo_type = request.POST.get('type')
            obj = Todos.get_todo_by_id(todo_id)
            obj.status = todo_type
            obj.save()
            response['current'] = (obj.title, obj.deadline.strftime("%I:%M%p on %B %d, %Y"), obj.id, obj.priority)
            response['result'] = "Success"
            response['amount_of_todos'] = Todos.get_amounts(request.user)
        else:
            response['result'] = "User is not authenticated"
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseRedirect('/')


@login_required
def edit_todo(request):
    response = {}
    if request.method == "POST":
        form = EditTodoForm(request.POST)
        if form.is_valid():
            todo_id = form.cleaned_data['todo_id']
            deadline_date = form.cleaned_data['todo_edit_deadline']
            deadline_time = form.cleaned_data['todo_edit_time']
            deadline_date = datetime(deadline_date.year, deadline_date.month, deadline_date.day, deadline_time.hour, deadline_time.minute, 0)
            if deadline_date > datetime.now():
                if Todos.objects.filter(id=todo_id).exists():
                    tmp = Todos.get_todo_by_id(todo_id)
                    tmp.title = form.cleaned_data['todo_edit_title']
                    tmp.text = form.cleaned_data['todo_edit_text']
                    tmp.priority = form.cleaned_data['todo_edit_priority']
                    tmp.deadline = deadline_date
                    tmp.save()
                    response['result'] = "Success"
                    response['deadline_date'] = tmp.deadline.strftime("%I:%M%p on %B %d, %Y")
                    response['priority'] = tmp.priority
                else:
                    response['result'] = 'No such todo'
            else:
                response['result'] = 'Date has already passed'
        else:
            response['result'] = 'Form is not valid'
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def read_file(file_name):
    s = open(file_name, "r")
    s = s.read()
    a = s.split("\n")
    user = a[0]
    date, time = '00-00-00', '34'
    if not (a[1]):
        added_time = time
    else:
        added_time = a[1]
    if not (a[2]):
        added_date = date
    else:
        added_date = a[2]
    priority = a[3]
    if not (a[4]):
        status = "in progress"
    else:
        status = a[4]
    deadline = a[5]
    text = a[6]
    title = a[7]
    p = Todos(text=text, user=user, title=title, added_time=added_time,
              added_date=added_date, priority=priority, deadline=deadline, status=status)
    p.save()


@login_required
def delete_todo(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            todo_id = request.POST.get('id')
            if Todos.delete_todo(todo_id):
                result = "Success"
            else:
                result = "Sorry, Todo does not exist"
        else:
            result = 'user is not authenticated'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def search(request):
    response_data = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            form = SearchForm(request.POST)
            if form.is_valid():
                string = form.data['result']
                response_data = {
                    'todo_list': Todos.search_todos(string, request.user)
                }
                result = 'Success'
            else:
                result = 'Form is not valid'
        else:
            result = 'user is not authenticated'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def check_notify():
    for tmp_user in User.objects.all():
        for tmp_todo in Todos.objects.filter(user=tmp_user):
            if datetime(0, 0, 0, 1, 0, 0, 0) > tmp_todo.deadline - datetime.now():
                mail = create_mail(tmp_user, "У вас не выполненная задача!" + tmp_todo.title, "У вас не выполненная задача!")
                send_mail(mail)
