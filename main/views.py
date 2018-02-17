from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.forms import *


def index(request):
    context = {
        'title': "Index page",
        'header': "Index page header",
    }
    return render(request, "main/index.html", context)


def login_view(request):
    context = {}
    if request.POST:
        form = AuthForm(request.POST)
        if form.is_valid():
            pattern = compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
            if pattern.match(form.data['username'].lower()):
                tmp = User.objects.filter(email=form.data['username'].lower()).first().username
            else:
                tmp = form.data['username'].lower()
            user = authenticate(request, username=tmp, password=form.data['password'])
            if user is not None:
                login(request, user)
                context['title'] = 'Index page'
                context['header'] = 'Index page header'
                messages.add_message(request, messages.INFO, context)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse('Username or email or password not correct. Go to <a href="/">main</a>.')
        else:
            return HttpResponse('Login failed. Sorry. Go to <a href="/">main</a>.')
    else:
        pass


def logout_view(request):
    logout(request)
    context = {'index_text': 'Welcome to out simple voteapp'}
    context['user'] = request.user
    messages.add_message(request, messages.INFO, context)
    return HttpResponseRedirect('/')
