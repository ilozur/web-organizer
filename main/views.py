from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.forms import *
import json


def index(request):
    context = {
        'title': "Index page",
        'header': "Index page header",
    }
    if not request.user.is_authenticated:
        login_form = AuthForm()
        context['login_form'] = login_form
    return render(request, "main/index.html", context)


def login_ajax(request):
    response_data = {}
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            name = form.data['username'].lower()
            password = form.data['password']
            found_user = (len(User.objects.filter(username=name)) > 0) or \
                         (len(User.objects.filter(email=name)) > 0)
            if not found_user:
                result = "User not found"
            else:
                user = User.objects.filter(email=name).first()
                if user is None:
                    user = User.objects.filter(username=name).first()
                loginned_user = authenticate(request, username=user.username, password=password)
                if loginned_user is None:
                    result = "Wrong password"
                else:
                    login(request, loginned_user)
                    result = "Success"
        else:
            result = "Form not valid"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
