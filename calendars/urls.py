from django.urls import path

from calendars.views import *

urlpatterns = [
    path('', index, name='calendar.index'),
]
