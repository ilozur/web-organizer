from calendars.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import *
from datetime import datetime
from calendars.forms import *
from django.http import HttpResponse
import json


@login_required
def index(request):
    context = {
        'title': "Calendar index page",
        'header': "Calendar index page header",
    }
    just_added_event = 'just_added_event' in dict(request.GET)
    context['just_added_event'] = just_added_event
    return render(request, "calendars/index.html", context)



@login_required
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
