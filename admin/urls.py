from django.urls import path

from admin.views import *

urlpatterns = [
    path('', index, name='admin.index'),
]