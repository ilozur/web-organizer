from calendars.models import *
from django.shortcuts import render
from django.contrib.auth.decorators import *
from datetime import datetime


def index(request):
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
def add_event(data):
    time_now = datetime.now()
    data['date'] = time_now.date()
    data['time'] = time_now.time()
    event = Event(user=data['user'], date=data['date'], time=data['time'], title=data['title'],
                  description=data['description'], is_public=data['is_public'])
    event.save()
