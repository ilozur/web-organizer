from django.shortcuts import render
from main.forms import SignInForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
import json


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
        return HttpResponseRedirect('/')
