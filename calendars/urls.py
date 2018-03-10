from django.urls import path

from calendars.views import *

urlpatterns = [
    path('', index, name='calendar.index'),
    path('<str:date>', index_date, name='calendar.index_date'),
    path('event/add', event_view, name='calendar.event_view'),
]
