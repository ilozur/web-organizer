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
from ckeditor_uploader import views
import calendars.urls
import notes.urls
import todo.urls
import profile.urls
from main.views import *
from django.conf.urls.static import static
from morris_butler import settings
from django.contrib.auth.decorators import login_required

from profile.views import confirm_mail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('notes/', include(notes.urls)),
    path('calendar/', include(calendars.urls)),
    path('todo/', include(todo.urls)),
    path('profile/', include(profile.urls)),
    path('sign_in/', sign_in_ajax, name='sign_in'),
    path('sign_out/', sign_out_view, name='sign_out'),
    path('sign_up/', sign_up_view, name='sign_up'),
    path('activate/<str:key>', activate_key, name='activate_key'),
    path('confirm_mail/<str:key>', confirm_mail, name='confirm_mail'),
    path('ckeditor/upload/', login_required(views.upload), name='ckeditor_upload'),
    # path('notes_latest/',include(notes.urls)),
    # path('todo_near',include(todo.urls)),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
