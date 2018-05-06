from django.contrib.auth.models import User
from django.shortcuts import render
from main.forms import SignInForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
import json
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
    context = {'sign_in_form': SignInForm()}
    return render(request, "admin/index.html", context)


def sign_in_ajax(request):
    response_data = {}
    if request.method == "POST":
        if not request.user.is_authenticated:
            form = SignInForm(request.POST)
            if form.is_valid():
                name = form.data['username_sign_in'].lower()
                password = form.data['password']
                found_user = (len(User.objects.filter(username=name)) > 0) or \
                             (len(User.objects.filter(email=name)) > 0)
                if not found_user:
                    result = "106"
                else:
                    user = User.objects.filter(email=name).first()
                    if user is None:
                        user = User.objects.filter(username=name).first()
                    if user.is_active:
                        if user.is_superuser:
                            loginned_user = authenticate(request, username=user.username, password=password)
                            if loginned_user is None:
                                result = "107"
                            else:
                                login(request, loginned_user)
                                result = "100"
                        else:
                            result = "106"
                    else:
                        result = "108"
            else:
                result = "104"
        else:
            result = "105"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        context = {}
        users = User.objects.all()
        if request.method == 'POST':
            if request.key == 'uc':
                user_create(request.logfld, request.passfld, request.langfld)
            elif request.key == 'c':
                creation(request.checkbox, request.inputfld, users)
        return render(request, "admin/index.html", context)

def info(request):
    list_user = User.objects.all()
    context = {
        "list_user": list_user
    }
    return render(request, "admin/info.html", context)
