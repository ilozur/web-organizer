from django.urls import path

from siteprofile.views import *

urlpatterns = [
    path('', index, name='siteprofile.index'),
    path('change_user_data', change_user_data_ajax, name='siteprofile.change_user_data'),
    path('change_password', change_password_ajax, name='siteprofile.change_password'),
    path('get_user_data', get_user_data_ajax, name='siteprofile.get_user_data'),
    path('recover_password_key', create_recover_password_key_ajax, name='siteprofile.recover_password_key'),
    path('recover_password/<str:key>', recover_password_view, name='siteprofile.recover_password'),
    path('recover_password_ajax/<str:key>', recover_password_ajax, name='siteprofile.recover_password_ajax')
]
