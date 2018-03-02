from calendars.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import *
from datetime import datetime
from main.notifier import *


def index(request):
    notify_if_needed()
    context = {
        'title': "Calendar index page",
        'header': "Calendar index page header",
    }
    return render(request, "calendars/index.html", context)


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


@login_required
def add_event(request, data):
    time_now = datetime.now()
    data['added_date'] = time_now.date()
    data['added_time'] = time_now.time()
    data['user'] = request.user
    event = Event(user=data['user'], date=data['date'], time=data['time'], title=data['title'],
                  description=data['description'], is_public=data['is_public'],
                  added_date=data['added_date'], added_time=data['added_time'], status="opened",
                  should_notify_hours=data['should_notify_hours'], should_notify_minutes=data['should_notify_minutes'],
                  should_notify_days=data['should_notify_days'])
    event.save()
