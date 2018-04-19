from calendars.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import *
from datetime import datetime, timedelta
from calendars.forms import *
from main.models import Language
from django.http import HttpResponse, HttpResponseRedirect
import json


@login_required
def index(request):
    if request.method == "GET":
        date = datetime.now()
        context = dict(title="Calendar index page", header="Calendar index page header")
        context['weeks'] = get_weeks(date, request.user)
        context['all_events_count'] = Event.objects.filter(user=request.user).count()
        context['today_events_count'] = Event.objects.filter(user=request.user, date=date.date()).count()
        context['yesterday_events_count'] = Event.objects.filter(user=request.user,
                                                                 date=date.date() - timedelta(1)).count()
        context['week_events_count'] = Event.get_events_in_range(date.date() - timedelta(7),
                                                                 date.date(), request.user).count()
        context['month_events_count'] = Event.get_events_in_range(date.date() - timedelta(30),
                                                                  date.date(), request.user).count()
        context['year_events_count'] = Event.get_events_in_range(date.date() - timedelta(365),
                                                                 date.date(), request.user).count()
        context['now_month'] = get_month_name(date.month)
        context['now_year'] = date.year
        context['now_month_num'] = date.month
        context['now_date'] = str(date.year) + "_" + str(date.month)
        add_event_form = AddingEventForm()
        context['add_event_form'] = add_event_form
        context['language'] = Language.objects.filter(user=request.user).first().lang
        return render(request, "calendars/index.html", context)
    else:
        response_data = {}
        datetime_now = datetime.now()
        try:
            now_date_string = request.POST.get('now_date', '')
            tmp = now_date_string.split('_')
            tmp = [int(num) for num in tmp]
            if len(tmp) == 2:
                if (datetime_now.month == tmp[1]) and (datetime_now.year == tmp[0]):
                    now_date = datetime(year=tmp[0], month=tmp[1], day=datetime_now.day)
                else:
                    now_date = datetime(year=tmp[0], month=tmp[1], day=1)
            else:
                return HttpResponse(json.dumps({'result': 'failed'}), content_type="application/json")
        except ValueError:
            return HttpResponse(json.dumps({'result': 'failed'}), content_type="application/json")
        response_data['weeks'] = get_weeks(now_date, request.user)
        response_data['month_name'] = get_month_name(now_date.month)
        response_data['now_year'] = now_date.year
        response_data['result'] = "100"
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def get_weeks(date_time, user):
    date = date_time
    datetime_now = datetime.now()
    if (date.month == datetime_now.month) and (date.year == datetime_now.year):
        now_month = True
    else:
        now_month = False
    date -= timedelta(days=date.weekday())
    if (date.day > 1) and (date.month == date_time.month):
        date -= timedelta(days=7 * (date.day // 7))
        if date.month == date_time.month:
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
            tmp_day_events = Event.objects.filter(user=user, date=date)
            if tmp_day_events.count() > 0:
                tmp_day['event'] = {'caption': tmp_day_events[0].title, 'id': tmp_day_events[0].id}
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
            tmp_day_events = Event.objects.filter(user=user, date=date)
            if tmp_day_events.count() > 0:
                tmp_day['event'] = {'caption': tmp_day_events[0].title, 'id': tmp_day_events[0].id}
            week_days.append(tmp_day)
            date += timedelta(days=1)
        tmp['week_days'] = week_days
        weeks.append(tmp)
    return weeks


def get_month_name(month):
    m = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
         "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь", ]
    return m[month - 1]


def search_events(string):
    events = Event.get_events("title_up_all")
    found_events = []
    for i in events:
        if i.title.find(string) != -1:
            found_events.append(i)
    return found_events


def add_event(request, data):
    time_now = datetime.now()
    data['added_date'] = time_now.date()
    data['added_time'] = time_now.time()
    if data['should_notify_hours'] is None:
        data['should_notify_hours'] = 0
    if data['should_notify_days'] is None:
        data['should_notify_days'] = 0
    if data['should_notify_minutes'] is None:
        data['should_notify_minutes'] = 0
    data['user'] = request.user
    if time_now > datetime(data['date'].year, data['date'].month, data['date'].day, data['time'].hour,
                           data['time'].minute, data['time'].second):
        return "109"
    else:
        if (data['should_notify_hours'] < 0) or (data['should_notify_minutes'] < 0) or (data['should_notify_days'] < 0):
            return "110"
        else:
            event = Event(user=data['user'], date=data['date'], time=data['time'], title=data['title'],
                          description=data['description'], is_public=data['is_public'],
                          added_date=data['added_date'], added_time=data['added_time'], status="opened",
                          should_notify_hours=data['should_notify_hours'],
                          should_notify_minutes=data['should_notify_minutes'],
                          should_notify_days=data['should_notify_days'])
            event.save()
            return "100"


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
            response_data['result'] = "104"
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def get_event_data_ajax(request):
    response_data = {}
    if request.method == "POST":
        event_id = request.POST.get('id')
        if Event.objects.filter(user=request.user, id=event_id).count() > 0:
            event = Event.objects.filter(id=event_id).first()
            response_data = {
                'title': event.title,
                'description': event.description,
                'date': datetime.combine(event.date, event.time).strftime("%I:%M%p on %B %d, %Y"),
            }
            result = '100'
        else:
            result = '114'
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def delete_ajax(request):
    response_data = {}
    if request.method == "POST":
        event_id = request.POST.get('id')
        if Event.objects.filter(user=request.user, id=event_id).count() > 0:
            if Event.delete_event(event_id):
                result = "100"
            else:
                result = "114"
        else:
            result = "114"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')
