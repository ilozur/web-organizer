from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import main.management.commands.generate_notes as gn
import main.management.commands.generate_events as ge
import main.management.commands.generate_todo as gt
import main.management.commands.generate_users as gu
import main.management.commands.createuser as cu
from admin.forms import CForm, ucform


def creation(argument, number, users):
    number = int(number)
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
        c = gu.Command()
        for i in range(0, number):
            gu.Command.create_user(c)


def user_create(nickname, password, lang):
    cu.Command.create_user(nickname, password, lang)


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    context = {}
    req = request.POST
    users = User.objects.all()
    if req:
        if 'logfld' in req:
            user_create(req['logfld'], req['passfld'], req['langfld'])
        elif 'inputfld' in req:
            cf = CForm(req)
            creation(cf.data['choicebox'], cf.data['inputfld'], users)
    cf = CForm()
    ucf = ucform()
    context['cform'] = cf
    context['ucform'] = ucf
    return render(request, "admin/index.html", context)


def info(request):
    list_user = User.objects.all()
    context = {
        "list_user": list_user
    }
    return render(request, "admin/info.html", context)
