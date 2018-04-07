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
    response_data = {}
    user = request.user
    if request.method == "POST":
        form = ChangeUserDataForm(request.POST)
        if form.is_valid():
            last_name = form.cleaned_data['surname']
            first_name = form.cleaned_data['name']
            if not modification_of_user_data(request.user, name=first_name, surname=last_name):
                result = "Error"
                response_data['answer'] = "Это имя пользователя уже используется"
                response_data['result'] = result
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            email = form.cleaned_data['email']
            if email != request.user.email:
                confirm_email_key = create_confirm_email_key(user, email)
                if confirm_email_key is None:
                    result = "Error"
                    response_data['answer'] = "Эта эл. почта уже используется другим пользователем"
                else:
                    mail = create_mail(user,
                                       "Перейдите по этой ссылке для подтверждения почты: 127.0.0.1:8000/confirm_mail/" +
                                       confirm_email_key.key, "<a href='http://127.0.0.1:8000/confirm_mail/" +
                                       confirm_email_key.key + "'>Перейдите по этой ссылке для подтверждения почты</a>", email)
                    send_mail(mail)
                    result = "Готово!"
                    response_data['answer'] = "Проверьте эл.почту для подтверждения"
            else:
                result = "Готово!"
                response_data['answer'] = "Данные были изменены"
        else:
            result = 'Error'
            response_data['answer'] = "Форма недействительна"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def confirm_mail(request, key):
    if request.method == "GET":
        keys = ConfirmMailKey.objects.filter(key=key)
        if keys.count() > 0:
            user = keys.first().user
            user.email = keys.first().email
            keys.first().delete()
            user.save()
    return HttpResponseRedirect('/profile')


def create_confirm_email_key(user, email):
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
                    result = "Готово"
                else:
                    result = "Новые пароли не совпадают"
            else:
                result = "Неверный пароль"
        else:
            result = "Поле недействительно"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def recover_password_view(request, key):
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
                        result = "Готово!"
                    else:
                        result = "Этот пользователь не активирован"
                else:
                    result = "Неверный ключ"
            else:
                result = "Пароли не совпадают"
        else:
            result = "Поле недействительно"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseRedirect('/')


def create_recover_password_key_ajax(request):
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
                                           "Перейдите по этой ссылке для восстановления пароля: 127.0.0.1:8000/profile/recover_password/" +
                                           key.key,
                                           "<a href='http://127.0.0.1:8000/profile/recover_password/" + key.key +
                                           "'>Перейдите по этой ссылке для восстановления пароля</a>")
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
