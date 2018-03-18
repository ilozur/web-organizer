from django.urls import path

from profile.views import *

urlpatterns = [
    path('', index, name='profile.index'),
    path('change_user_data', change_user_data_ajax, name='profile.change_user_data'),
    path('change_password', change_password_ajax, name='profile.change_password'),
    path('get_user_data', get_user_data_ajax, name='profile.get_user_data'),
]
