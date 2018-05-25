from django.urls import path

from userprofile.views import *

urlpatterns = [
    path('', index, name='userprofile.index'),
    path('change_user_data', change_user_data_ajax, name='userprofile.change_user_data'),
    path('change_user_data', change_user_data_ajax, name='userprofile.change_user_data'),
    path('change_language', change_language_ajax, name='userprofile.change_language'),
    path('get_user_data', get_user_data_ajax, name='userprofile.get_user_data'),
    path('recover_password_key', create_recover_password_key_ajax, name='userprofile.recover_password_key'),
    path('recover_password/<str:key>', recover_password_view, name='userprofile.recover_password'),
    path('recover_password_ajax/<str:key>', recover_password_ajax, name='userprofile.recover_password_ajax')
]
