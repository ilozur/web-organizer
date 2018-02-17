from django.shortcuts import render
from calendars.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


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
