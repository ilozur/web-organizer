from django.urls import path

from admin.views import *

urlpatterns = [
    path('', index, name='admin.index'),
    path('sign_in/', sign_in_ajax, name='admin.sign_in'),
]
