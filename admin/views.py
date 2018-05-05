from django.contrib.auth.models import User
from django.shortcuts import render
import admin.forms as forms
from django.contrib.auth.decorators import user_passes_test
import main.management.commands.generate_notes as gn
import main.management.commands.generate_events as ge
import main.management.commands.generate_todo as gt
import main.management.commands.generate_users as gu
import main.management.commands.createuser as cu


# Register your models here.


def creation(argument, number, users):
    if argument == 'n' or argument == 'N':
        for i in range(0, number):
            for user in users:
                gn.Command.create_note(user)
    elif argument == 'e' or argument == 'E':
        for i in range(0, number):
            for user in users:
                ge.Command.create_event(user)
    elif argument == 't' or argument == 'T':
        for i in range(0, number):
            for user in users:
                gt.Command.create_todo(user)
    elif argument == 'u' or argument == 'U':
        for i in range(0, number):
            for user in users:
                gu.Command.create_user(user)


def user_create(nickname, password, lang):
    cu.Command.create_user(nickname, password, lang)


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    context = {}
    cform = forms.cform()
    users = User.objects.all()
    if request.method == 'POST':
        if request.key == 'uc':
            user_create(request.nickname, request.password, request.lang)
        elif request.key == 'c':
            creation(request.argument, request.number, users)
    return render(request, "admin/index.html", context)


def info(request):
    list_user = User.objects.all()
    context = {
        "list_user": list_user
    }
    return render(request, "admin/info.html", context)
