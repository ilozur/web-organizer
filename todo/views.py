from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from main.models import Language
from main.views import create_mail, send_mail
from todo.forms import AddTodoForm
from todo.forms import SearchForm
from todo.forms import EditTodoForm
from todo.models import Todos
import json
from datetime import datetime
from localisation import eng, rus
type_of_sort = 'AtoZ'


@login_required
def index(request):
    sort_type = request.GET.get("sort_type", "new")
    todo = Todos.get_todos(sort_type, request.POST.get('status'), user=request.user)
    page = request.GET.get("page")
    try:
        page = int(page)
    except Exception as ex:
        page = 1
        print(ex)
    if request.method == "GET":
        context = {
            'title': "Todos index page",
            'header': "Todos index page header",
        }
        user_lang = Language.objects.filter(user=request.user).first().lang
        if user_lang == "ru":
            lang = rus
        elif user_lang == "en":
            lang = eng
        else:
            lang = eng
        context['language'] = user_lang
        context['lang'] = lang
        user = request.user
        pages = Paginator(todo, 20)
        if (page < 1) or (page > len(pages.page_range)):
            page = 1
        context['page'] = page
        context['todo_data'] = pages.page(page)
        context['back_paginate_btn'] = pages.page(page).has_previous()
        context['next_paginate_btn'] = pages.page(page).has_next()
        context['todo_pages'] = pages.page_range
        done_todos = Paginator(Todos.get_todos('AtoZ', 'done', user), 20)
        context['done_todos'] = done_todos.page(1).object_list
        context['done_pages'] = done_todos.page_range
        context['amount_of_todos'] = Todos.get_amounts(user)
        context['search_todo_form'] = SearchForm()
        context['add_todo_form'] = AddTodoForm()
        context['edit_todo_form'] = EditTodoForm()
        return render(request, "todo/index.html", context)


@login_required
def add_todo(request):
    user = request.user
    response_data = {}
    if request.method == "POST":
        form = AddTodoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['todo_title']
            deadline_date = form.cleaned_data['todo_deadline']
            deadline_time = form.cleaned_data['todo_time']
            deadline_date = datetime(deadline_date.year, deadline_date.month, deadline_date.day, deadline_time.hour,
                                     deadline_time.minute, 0)
            if deadline_date > datetime.now():
                tmp = Todos(title=title, added_date_and_time=datetime.now(), user=request.user,
                            priority=form.cleaned_data['todo_priority'], deadline=deadline_date)
                tmp.smart_priority = smart_priority(tmp, 'add', user)
                tmp.save()
                result = "Success"
                response_data['id'] = tmp.id
                response_data['title'] = tmp.title
                response_data['datetime'] = datetime.now().strftime("%I:%M%p on %B %d, %Y")
                response_data['priority'] = tmp.priority
                response_data['smart_priority'] = tmp.smart_priority
            else:
                result = 'Deadline date has passed'
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
                'added_date_and_time': todo.added_date_and_time.strftime("%I:%M%p on %B %d, %Y"),
                'deadline': todo.deadline.strftime("%I:%M%p on %B %d, %Y"),
                'priority': todo.priority,
                'status': todo.status,
                'time': [todo.deadline.hour, todo.deadline.minute],
                'date': [todo.deadline.year, todo.deadline.month, todo.deadline.day],
                'id': todo.id,
                'result': "Success",
                'current_status': current_status,
                'smart_priority': todo.smart_priority
            }
        else:
            response = {
                'result': "User is not authenticated"
            }
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def sorting(request):
    response = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            sort_type = request.POST.get('data')
            response = {
                'todo_list': Todos.get_todos(sort_type, 'in progress', request.user, 'none'),
                'result': "Success"
            }
            global type_of_sort
            type_of_sort = sort_type
        else:
            response['result'] = "User is not authenticated"
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def status_change(request):
    response = {}
    if request.method == "POST":
        todo_id = request.POST.get('id')
        todo_type = request.POST.get('type')
        obj = Todos.get_todo_by_id(todo_id)
        obj.status = todo_type
        obj.save()
        response['current'] = (obj.title, obj.deadline.strftime("%I:%M%p on %B %d, %Y"), obj.id, obj.priority)
        response['result'] = "Success"
        response['amount_of_todos'] = Todos.get_amounts(request.user)
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return HttpResponseRedirect('/')


@login_required
def edit_todo(request):
    user = request.user
    response = {}
    if request.method == "POST":
        form = EditTodoForm(request.POST)
        if form.is_valid():
            todo_id = form.cleaned_data['todo_id']
            deadline_date = form.cleaned_data['todo_edit_deadline']
            deadline_time = form.cleaned_data['todo_edit_time']
            deadline_date = datetime(deadline_date.year, deadline_date.month, deadline_date.day, deadline_time.hour,
                                     deadline_time.minute, 0)
            if deadline_date > datetime.now():
                if Todos.objects.filter(id=todo_id).exists():
                    tmp = Todos.get_todo_by_id(todo_id)
                    tmp.title = form.cleaned_data['todo_edit_title']
                    tmp.priority = form.cleaned_data['todo_edit_priority']
                    tmp.deadline = deadline_date
                    tmp.save()
                    response['result'] = "Success"
                    response['deadline_date'] = tmp.deadline.strftime("%I:%M%p on %B %d, %Y")
                    response['priority'] = tmp.priority
                    smart_priority(user)
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
    title = a[7]
    p = Todos(user=user, title=title, added_time=added_time,
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
                mail = create_mail(tmp_user, "У вас не выполненная задача!" + tmp_todo.title,
                                   "У вас не выполненная задача!")
                send_mail(mail)


def smart_priority(todo, address, user):
    now = datetime.now()
    now = now.strftime("%d.%m.%y")
    now = now.split('.')
    now = days_in_years(now)
    if address == 'index':
        deadline = todo[1]
        priority = todo[3]
        deadline = deadline.split('.')
        deadline = days_in_years(deadline) - now
        value = deadline*0.4+priority*0.6
        new_value = 100-round(((value - 1) / (max_smart_priority(user, now) - 1)) * (100 - 1) + 1)
        if new_value == 0:
            new_value +=1
        tmp = Todos.get_todo_by_id(todo[2])
        tmp.smart_priority = new_value
        tmp.save()
    elif address == 'add':
        deadline = todo.deadline
        priority = todo.priority
        deadline = deadline.strftime("%d.%m.%y")
        deadline = deadline.split('.')
        deadline = days_in_years(deadline) - now
        value = deadline * 0.4 + priority * 0.6
        new_value = 100-round(((value - 1) / (max_smart_priority(user, now) - 1)) * (100 - 1) + 1)
        if new_value == 0:
            new_value +=1
        return new_value


def paginate(todo, page_number):

    response_data = {}
    pages = Paginator(todo, 20)
    if (page_number < 1) or (page_number > len(pages.page_range)):
        page_number = 1
    response_data['buttons'] = [pages.page(page_number).has_previous(), pages.page(page_number).has_next()]
    response_data['todo_list'] = pages.page(page_number).object_list
    response_data['result'] = 100
    response_data['normal_page'] = page_number
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def days_in_years(tmp):
    result = 0
    statistic = {
        '1': 31,
        '3': 31,
        '4': 30,
        '5': 31,
        '6': 30,
        '7': 31,
        '8': 31,
        '9': 30,
        '10': 31,
        '11': 30,
        '12': 31,
    }
    if (int(tmp[2]) % 4 == 0) and (int(tmp[2]) % 100 != 0) or (int(tmp[2]) % 400 == 0):
        statistic['2'] = 29
        year = 366
    else:
        statistic['2'] = 28
        year = 365
    for item in range(1, int(tmp[1])):
        result += int(statistic[str(item)])
    result += year*int(tmp[2]) + int(tmp[0])
    return result


def max_smart_priority(user, now):
    todo_list = Todos.get_todos('AtoZ', 'in progress', user, 'sm_priority')
    max = 0
    for item in todo_list:
        todo = item
        deadline = todo[1]
        priority = todo[3]
        deadline = deadline.split('.')
        deadline = days_in_years(deadline)-now
        value = 0.4*deadline+priority*0.6
        if value > max:
            max = value
    return max
