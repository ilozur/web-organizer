from django.urls import path

from calendars.views import *

urlpatterns = [
    path('events/add', event_view, name='calendar.event_view'),
    path('events/get_event_data', get_event_data_ajax, name='calendar.get_event_data'),
    path('events/delete', delete_ajax, name='calendar.delete')
]
