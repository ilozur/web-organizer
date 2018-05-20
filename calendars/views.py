import json

from django.contrib.auth.decorators import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from calendars.forms import *
from calendars.models import *
from localisation import rus, eng
from main.models import Language


@login_required
def index(request):
    """!
       @brief This function render calendar page for current user
    """
    if request.method == "GET":
        context = dict(title="Calendar index page", header="Calendar index page header")
        user_lang = Language.objects.filter(user=request.user).first().lang
        if user_lang == "ru":
            lang = rus
        elif user_lang == "en":
            lang = eng
        else:
            lang = eng
        context['language'] = user_lang
        context['lang'] = lang
        context['stat'] = Event.create_calendar_statistics(request)
        add_event_form = AddingEventForm()
        context['add_event_form'] = add_event_form
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
        events = Event.objects.filter(user=request.user)
        response_data['weeks'] = Event.get_weeks(now_date, request.user, events)
        response_data['month_name'] = Event.get_month_name(now_date.month)
        response_data['now_year'] = now_date.year
        response_data['result'] = "100"
        return HttpResponse(json.dumps(response_data), content_type="application/json")




def search_events(string):
    """!
        @brief This function select events by regular phrase
    """
    events = Event.get_events("title_up_all")
    found_events = []
    for i in events:
        if i.title.find(string) != -1:
            found_events.append(i)
    return found_events


def add_event(request, data):
    """!
        @brief This function add event to DB if data of event is valid
    """
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
            if data['place'] != "":
                event.place = data['place']
            print(event.place)
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
    """!
        This function get data of event (with ajax)
    """
    response_data = {}
    if request.method == "POST":
        event_id = request.POST.get('id')
        if Event.objects.filter(user=request.user, id=event_id).count() > 0:
            event = Event.objects.filter(id=event_id).first()
            response_data = {
                'title': event.title,
                'description': event.description,
                'date': datetime.combine(event.date, event.time).strftime("%I:%M%p on %B %d, %Y"),
                'map_coordinates': event.place,
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
