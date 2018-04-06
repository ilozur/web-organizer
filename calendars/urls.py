from django.urls import path

from calendars.views import *

urlpatterns = [
    path('', index, name='calendar.index'),
    path('events/add', event_view, name='calendar.event_view'),
    path('get_event_data', get_event_data_ajax, name='calendar.get_event_data'),
]
