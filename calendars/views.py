from calendars.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import *
from datetime import datetime, timedelta
from calendars.forms import *
from django.http import HttpResponse, HttpResponseRedirect
import json


@login_required
def index(request):
    if request.method == "GET":
        date = datetime.now()
        return HttpResponseRedirect('/calendar/' + str(date.year) + '_' + str(date.month) + '_' + str(date.day))
    else:
        return HttpResponseRedirect('/calendar/')


@login_required
def index_date(request, date):
    if request.method == "GET":
        context = dict(title="Calendar index page", header="Calendar index page header")
        try:
            tmp = date.split('_')
            tmp = [int(num) for num in tmp]
            if len(tmp) == 3:
                now_date = datetime(year=tmp[0], month=tmp[1], day=tmp[2])
            elif len(tmp) == 2:
                now_date = datetime(year=tmp[0], month=tmp[1], day=1)
            else:
                return HttpResponseRedirect('/calendar/')
        except ValueError:
            return HttpResponseRedirect('/calendar/')
        context['weeks'] = get_weeks(now_date)
        context['now_month'] = get_month_name(now_date.month)
        context['now_year'] = now_date.year
        datetime_now = datetime.now()
        if now_date.month == 1:
            back_link = str(now_date.year - 1) + '_12'
            if (12 == datetime_now.month) and (now_date.year - 1 == datetime_now.year):
                back_link += '_' + str(datetime_now.day)
        else:
            back_link = str(now_date.year) + '_' + str(now_date.month - 1)
            if (now_date.month - 1 == datetime_now.month) and (now_date.year == datetime_now.year):
                back_link += '_' + str(datetime_now.day)
        if now_date.month == 12:
            next_link = str(now_date.year + 1) + '_1'
            if (1 == datetime_now.month) and (now_date.year + 1 == datetime_now.year):
                next_link += '_' + str(datetime_now.day)
        else:
            next_link = str(now_date.year) + '_' + str(now_date.month + 1)
            if (now_date.month + 1 == datetime_now.month) and (now_date.year == datetime_now.year):
                next_link += '_' + str(datetime_now.day)
        context['back_link'] = back_link
        context['next_link'] = next_link
        context['now_date'] = str(datetime_now.year) + '_' + str(datetime_now.month) + '_' + str(datetime_now.day)
        return render(request, "calendars/index.html", context)
    else:
        return HttpResponseRedirect('/calendar/')


def get_month_name(month):
    result = ""
    if month == 1:
        result = "Январь"
    elif month == 2:
        result = "Февраль"
    elif month == 3:
        result = "Март"
    elif month == 4:
        result = "Апрель"
    elif month == 5:
        result = "Май"
    elif month == 6:
        result = "Июнь"
    elif month == 7:
        result = "Июль"
    elif month == 8:
        result = "Август"
    elif month == 9:
        result = "Сентябрь"
    elif month == 10:
        result = "Октябрь"
    elif month == 11:
        result = "Ноябрь"
    elif month == 12:
        result = "Декабрь"
    return result


def get_weeks(date_time):
    date = date_time
    datetime_now = datetime.now()
    if (date.month == datetime_now.month) and (date.year == datetime_now.year):
        now_month = True
    else:
        now_month = False
    date -= timedelta(days=date.weekday())
    if (date.day > 1) and (date.month == date_time.month):
        date -= timedelta(days=7 * (date.day // 7))
        date -= timedelta(days=7)
    weeks = []
    for i in range(1, 5):
        tmp = dict()
        tmp['week_num'] = i
        week_days = []
        for day in range(1, 8):
            tmp_day = dict()
            tmp_day['day'] = date.day
            day_class = ""
            if now_month:
                if (date.day == date_time.day) and (date.month == date_time.month):
                    day_class = "today"
                elif date.month != date_time.month:
                    day_class = "future-date"
            else:
                if date.month != date_time.month:
                    day_class = "future-date"
            tmp_day['class'] = day_class
            week_days.append(tmp_day)
            date += timedelta(days=1)
        tmp['week_days'] = week_days
        weeks.append(tmp)
    last_month = date.month
    while last_month == date.month:
        tmp = dict()
        tmp['week_num'] = len(weeks) + 1
        week_days = []
        for day in range(1, 8):
            tmp_day = dict()
            tmp_day['day'] = date.day
            day_class = ""
            if now_month:
                if (date.day == date_time.day) and (date.month == date_time.month):
                    day_class = "today"
                elif date.month != date_time.month:
                    day_class = "future-date"
            else:
                if date.month != date_time.month:
                    day_class = "future-date"
            tmp_day['class'] = day_class
            week_days.append(tmp_day)
            date += timedelta(days=1)
        tmp['week_days'] = week_days
        weeks.append(tmp)
    return weeks


def get_events(sorting_type, user=None):
    # if aim = 'date' -> 'up' = new-old, 'down' = old-new
    # if aim = 'title' -> 'up' = a-z, 'down' = z-a
    sort = sorting_type.split('_')
    aim = sort[0]
    direction = sort[1]
    modificator = sort[2]
    if user:
        events = Event.objects.filter(user=user)
    else:
        events = Event.objects.all()
    if aim == "date":
        if direction == "up":
            events = events.order_by('-date', '-time')
        elif direction == "down":
            events = events.order_by('date', 'time')
    elif aim == "title":
        if direction == "up":
            events = events.order_by('title')
        elif direction == "down":
            events = events.order_by('-title')
    if modificator == 'all':
        pass
    elif modificator == 'public':
        events = events.filter(is_public=1)
    elif modificator == 'private':
        events = events.filter(is_public=0)
    return events


def add_event(request, data):
    time_now = datetime.now()
    data['added_date'] = time_now.date()
    data['added_time'] = time_now.time()
    data['user'] = request.user
    if time_now > datetime(data['date'].year, data['date'].month, data['date'].day, data['time'].hour,
                           data['time'].minute, data['time'].second):
        return "Wrong date"
    else:
        if (data['should_notify_hours'] < 0) or (data['should_notify_minutes'] < 0) or (data['should_notify_days'] < 0):
            return "Wrong notification params"
        else:
            event = Event(user=data['user'], date=data['date'], time=data['time'], title=data['title'],
                          description=data['description'], is_public=data['is_public'],
                          added_date=data['added_date'], added_time=data['added_time'], status="opened",
                          should_notify_hours=data['should_notify_hours'],
                          should_notify_minutes=data['should_notify_minutes'],
                          should_notify_days=data['should_notify_days'])
            event.save()
            return "Success"


@login_required
def event_view(request):
    context = {}
    if request.method == "GET":
        context['title'] = "Event add page"
        context['header'] = "Event add page header"
        adding_form = AddingEventForm()
        context['adding_form'] = adding_form
        return render(request, "calendars/add_event.html", context)
    else:
        response_data = {}
        form = AddingEventForm(request.POST)
        if form.is_valid():
            result = add_event(request, form.cleaned_data)
            response_data['result'] = result
        else:
            response_data['result'] = "Form not valid"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
