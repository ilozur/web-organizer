"""morris_butler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ckeditor_uploader import urls

import calendars.urls
import notes.urls
import todolist.urls
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('notes/', include(notes.urls)),
    path('calendar/', include(calendars.urls)),
    path('todo/', include(todolist.urls)),
    path('sign_in/', sign_in_ajax, name='sign_in'),
    path('sign_out/', sign_out_view, name='sign_out'),
    path('sign_up/', sign_up_view, name='sign_up'),
    path('activate/<str:key>', activate_key, name='activate_key'),
    path('ckeditor/', include(urls)),
]
