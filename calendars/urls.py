from django.urls import path

from calendars.views import *

urlpatterns = [
    path('', index, name='calendar.index'),
    path('events/add', event_view, name='calendar.event_view'),
    path('latest', get_near_event, name='calendar.nearest')
]
