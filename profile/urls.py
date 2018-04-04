from django.urls import path

from profile.views import *

urlpatterns = [
    path('', index, name='profile.index'),
    path('change_user_data', change_user_data_ajax, name='profile.change_user_data'),
    path('change_password', change_password_ajax, name='profile.change_password'),
    path('get_user_data', get_user_data_ajax, name='profile.get_user_data'),
    path('get_user_data', create_recover_password_key_ajax, name='profile.recover_password_key'),
    path('recover_password/<str:key>', recover_password_view, name='profile.recover_password'),
    path('recover_password_ajax/<str:key>', recover_password_ajax, name='profile.recover_password_ajax')
]
