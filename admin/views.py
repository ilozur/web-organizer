from django.shortcuts import render

from admin.models import User


def index(request):
    context = {}
    list_user = []
    users = User.get_users()
    for i in range(users):
        list_user.append(i.userName,i.name, i.surname, i.added_time, i.is_voice, i.last_edit_time)
    context['user_data'] = list_user
    return render(request, "admin/index.html", context)



s