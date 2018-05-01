from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
import main.management.commands.generate_notes as gn
import main.management.commands.generate_events as ge
import main.management.commands.generate_todo as gt
import main.management.commands.generate_users as gu
import main.management.commands.createuser as cu

from admin.models import User


# Register your models here.


def creation ( argument, number, users ):
    if argument == 'n' or argument == 'N':
        for i in range ( 0, number ):
            for user in users:
                gn.Command.create_note ( user )
    elif argument == 'e' or argument == 'E':
        for i in range ( 0, number ):
            for user in users:
                ge.Command.create_event ( user )
    elif argument == 't' or argument == 'T':
        for i in range ( 0, number ):
            for user in users:
                gt.Command.create_todo ( user )
    elif argument == 'u' or argument == 'U':
        for i in range ( 0, number ):
            for user in users:
                gu.Command.create_user ( user )


def user_create ( nickname, password, lang ):
    cu.Command.create_user ( nickname, password, lang )


@user_passes_test ( lambda u: u.is_superuser )
def index ( request ):
    context = {}
    list_user = []
    users = User.get_users()
    for i in range(users):
        list_user.append(i.userName,i.name, i.surname, i.added_time, i.is_voice, i.last_edit_time)
    context['user_data'] = list_user
    if request.method == 'POST':
        if request.key == 'uc':
            user_create(request.nickname, request.password, request.lang)
        elif request.key == 'c':
            creation(request.argument, request.number, users)
    return render ( request, "admin/index.html", context )
