from django.urls import path

from calendars.views import index

urlpatterns = [
    path('', index, name='calendar.index'),
]
