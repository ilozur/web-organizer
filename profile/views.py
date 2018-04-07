import json
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from profile.forms import *
from main.models import *
from main.views import create_mail, send_mail, create_key, check_email_uniq, create_unic_key


@login_required
def index(request):
    """!
            @brief Function that renders user's profile page
    """
    if request.method == "GET":
        change_user_data_form = ChangeUserDataForm()
        change_password_form = ChangePasswordForm()
        context = {
            'title': "User profile page",
            'header': "User profile header",
            'change_user_data_form': change_user_data_form,
            'change_password_form': change_password_form
        }
        if request.user.is_authenticated:
            return render(request, "main/profile.html", context)
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


@login_required
def get_user_data_ajax(request):
    """!
            @brief Function that gets user's data (with ajax)
    """
    response_data = {}
    user = request.user
    if request.method == "POST":
        last_name = user.last_name
        first_name = user.first_name
        email = user.email
        user_data = {
            'name': first_name,
            'username': user.username,
            'email': email,
            'surname': last_name
        }
        response_data['user'] = user_data
        result = "Success"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


@login_required
def change_user_data_ajax(request):
    """!
            @brief Function that changes user's data (with ajax)
    """
    response_data = {}
    user = request.user
    if request.method == "POST":
        form = ChangeUserDataForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['surname']
            first_name = form.cleaned_data['name']
            if not modification_of_user_data(request.user, name=first_name, surname=last_name):
                result = "Error"
                response_data['answer'] = "This username is already taken"
                response_data['result'] = result
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            email = form.cleaned_data['email']
            if email != request.user.email:
                confirm_email_key = create_confirm_email_key(user, email)
                if confirm_email_key is None:
                    result = "Error"
                    response_data['answer'] = "Email is already used by other user"
                else:
                    mail = create_mail(user,
                                       "Go to this link to confirm this email: 127.0.0.1:8000/confirm_mail/" +
                                       confirm_email_key.key, "<a href='http://127.0.0.1:8000/confirm_mail/" +
                                       confirm_email_key.key + "'>Go to this link to confirm this email</a>", email)
                    send_mail(mail)
                    result = "Success"
                    response_data['answer'] = "Please check your new email to confirm it"
            else:
                result = "Success"
                response_data['answer'] = "Ok, data were changed "
        else:
            result = 'Error'
            response_data['answer'] = "Form is not valid"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def confirm_mail(request, key):
    """!
            @brief Function that processes mail confirmation
    """
    if request.method == "GET":
        keys = ConfirmMailKey.objects.filter(key=key)
        if keys.count() > 0:
            user = keys.first().user
            user.email = keys.first().email
            keys.first().delete()
            user.save()
    return HttpResponseRedirect('/profile')


def create_confirm_email_key(user, email):
    """!
            @brief Function that creates email confirmation key
    """
    key = create_key(user.username + user.password, user)
    if check_email_uniq(email):
        if ConfirmMailKey.objects.filter(user=user).count() > 0:
            confirm_email_key = ConfirmMailKey.objects.filter(user=user).first()
            confirm_email_key.key = key
            confirm_email_key.email = email
            confirm_email_key.save()
        else:
            confirm_email_key = ConfirmMailKey(user=user, key=key, email=email)
            confirm_email_key.save()
    else:
        confirm_email_key = None
    return confirm_email_key


@login_required
def change_password_ajax(request):
    """!
            @brief Function that changes password if new one is valid (with ajax)
    """
    response_data = {}
    user = request.user
    if request.method == "POST":
        form = ChangeUserDataForm(request.POST)
        if form.is_valid():
            password = form.data['old_password']
            new_password1 = form.data['new_password1']
            new_password2 = form.data['new_password2']
            if user.check_password(password):
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    login(request, user)
                    result = "Success"
                else:
                    result = "New passwords does not match"
            else:
                result = "Wrong password"
        else:
            result = "Form is not valid"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def recover_password_view(request, key):
    """!
            @brief Function that renders password recovery page
    """
    if request.method == "GET":
        recover_form = RecoverPasswordForm()
        context = {
            'title': "Recover password page",
            'header': "Recover password header",
            'recover_form': recover_form,
            'key': key
        }
        return render(request, "main/recover_password.html", context)
    else:
        return HttpResponseRedirect('/')


def recover_password_ajax(request, key):
    """!
            @brief Function that recovers password (with ajax)
    """
    if request.method == "POST":
        response_data = {}
        recover_form = RecoverPasswordForm(request.POST)
        if recover_form.is_valid:
            if recover_form.data['password1'] == recover_form.data['password2']:
                if ConfirmKey.objects.filter(key=key).count() >= 1:
                    user = ConfirmKey.objects.filter(key=key).first().user
                    if user.is_active:
                        password = recover_form.data['password1']
                        user.set_password(password)
                        user.save()
                        login(request, user)
                        result = "Success"
                    else:
                        result = "This user is not activated"
                else:
                    result = "Wrong key"
            else:
                result = "Passwords does not match"
        else:
            result = "Form is not valid"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def create_recover_password_key_ajax(request):
    """!
            @brief Function that creates password recovery key
    """
    if request.method == "POST":
        response_data = {}
        recover_form = RecoverPasswordUserData(request.POST)
        if recover_form.is_valid:
            name = recover_form.data['recover_name']
            email = recover_form.data['recover_email']
            user = User.objects.filter(username=name).first()
            if user is not None:
                if user.email == email:
                    if user.is_active:
                        key = create_unic_key(user, user.username, user.password)
                        key.save()
                        mail = create_mail(user,
                                           "Go to this link to recover your password: 127.0.0.1:8000/profile/recover_password/" +
                                           key.key,
                                           "<a href='http://127.0.0.1:8000/profile/recover_password/" + key.key +
                                           "'>Go to this link to recover your password</a>")
                        send_mail(mail)
                    result = "100"
                else:
                    result = "113"
            else:
                result = "106"
        else:
            result = "104"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')
