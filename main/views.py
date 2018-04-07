from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.forms import *
from main.models import *
import json
import hashlib
import binascii
from datetime import datetime, timedelta
from django.core.mail import EmailMultiAlternatives
from morris_butler.settings import SECRET_KEY, EMAIL_HOST_USER
from calendars.forms import AddingEventForm
from notes.forms import *
from notes.models import Notes
from django.contrib.auth.models import User

from profile.forms import RecoverPasswordUserData


def index(request):
    """!
            @brief Function that renders home page if user is authenticated and index page if not
    """
    if request.method == "GET":
        context = {
            'title': "Index page",
            'header': "Index page header",
        }
        if not request.user.is_authenticated:
            sign_in_form = SignInForm()
            context['sign_in_form'] = sign_in_form
            sign_up_form = SignUpForm()
            context['sign_up_form'] = sign_up_form
            recover_password_user_data_form = RecoverPasswordUserData()
            context['recover_password_form'] = recover_password_user_data_form
            return render(request, "main/index.html", context)
        else:
            context['add_event_form'] = AddingEventForm()
            context['add_note_form'] = AddNoteForm()
            context['edit_note_form'] = EditNoteForm()
            context['last_notes'] = get_last_notes(request.user)
            context['last_notes_count'] = len(context['last_notes'])
            return render(request, "main/home.html", context)
    else:
        return HttpResponseRedirect('/')


def get_last_notes(user):
    """!
            @brief Function that get last three notes out all
    """
    all_notes = Notes.get_notes("date_up", user)
    if all_notes.count() >= 3:
        first_three = all_notes[0:3]
    else:
        first_three = all_notes
    return first_three


def send_mail(mail):
    """!
            @brief Function that sends emails
    """
    subject = mail['subject']
    text_content = mail['text_content']
    from_email = mail['from_email']
    to_email = mail['to_email']
    html_content = mail['html_content']
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def sign_up_ajax(request):
    """!
            @brief Function that signs user up (with ajax)
    """
    context = {}
    if request.method == "GET":
        if not request.user.is_authenticated:
            context['title'] = "Sign up page"
            context['header'] = "Sign up page header"
            sign_up_form = SignUpForm()
            context['sign_up_form'] = sign_up_form
            return render(request, "main/sign_up.html", context)
        else:
            return HttpResponseRedirect('/')
    else:
        response_data = {}
        if not request.user.is_authenticated:
            form = SignUpForm(request.POST)
            if form.is_valid():
                email = form.data['email'].lower()
                username = form.data['username'].lower()
                name = form.data['name']
                surname = form.data['surname']
                pass1 = form.data['password1']
                pass2 = form.data['password2']
                email_uniq = check_email_uniq(email)
                username_uniq = check_username_uniq(username)
                if email_uniq:
                    if username_uniq:
                        if pass1 == pass2:
                            user = User(email=email, username=username, first_name=name, last_name=surname, is_active=0)
                            user.set_password(pass1)
                            user.save()
                            sign_up_key = create_unic_key(user, username, pass1)
                            sign_up_key.save()
                            mail = create_mail(user,
                                               "Go to this link to activate your account: 127.0.0.1:8000/activate/" +
                                               sign_up_key.key,
                                               "<a href='http://127.0.0.1:8000/activate/" + sign_up_key.key +
                                               "'>Go to this link to activate your account</a>")
                            send_mail(mail)
                            result = "100"
                        else:
                            result = "101"
                    else:
                        result = "102"
                else:
                    result = "103"
            else:
                result = "104"
        else:
            result = "105"
        response_data['result'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def create_mail(user, text, html, email=None):
    """!
            @brief Function that creates mail
    """
    mail = dict()
    mail['subject'] = 'Dear ' + user.first_name + ' ' + user.last_name + '!'
    mail['from_email'] = EMAIL_HOST_USER
    if email:
        mail['to_email'] = email
    else:
        mail['to_email'] = user.email
    mail['text_content'] = text
    mail['html_content'] = html
    return mail


def create_unic_key(user, username, password):
    """!
            @brief Function creates sign up key
    """
    key = create_key(username + password, user)
    expiration_date = datetime.now().date()
    expiration_date += timedelta(days=3)
    sign_up_key = ConfirmKey(user=user, key=key, expiration_date=expiration_date)
    return sign_up_key


def activate_key(request, key):
    """!
            @brief Function that activates key if it is valid
    """
    if request.method == "GET":
        keys = ConfirmKey.objects.filter(key=key)
        if keys.count() > 0:
            if keys.first().expiration_date >= datetime.now().date():
                user = keys.first().user
                user.is_active = True
                user.save()
                keys.first().delete()
                logout(request)
                login(request, user)
    return HttpResponseRedirect('/')


def check_email_uniq(email):
    """!
            @brief Function that checks if email is unique
    """
    return User.objects.filter(email=email).count() == 0


def check_username_uniq(username):
    """!
            @brief Function that checks if username is unique
    """
    return User.objects.filter(username=username).count() == 0


def sign_in_ajax(request):
    """!
            @brief Function that signs user in (with ajax)
    """
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
                        loginned_user = authenticate(request, username=user.username, password=password)
                        if loginned_user is None:
                            result = "107"
                        else:
                            login(request, loginned_user)
                            result = "100"
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


def create_key(text, user):
    """!
            @brief Function that creates key
    """
    prepared_hash_object = hashlib.pbkdf2_hmac(hash_name='sha256',
                                               password=text.encode('utf-8'),
                                               salt=SECRET_KEY.encode('utf-8'),
                                               iterations=100000)
    key = binascii.hexlify(prepared_hash_object)
    key = key.decode('utf-8')
    key += str(user.id)
    return key


def sign_out_view(request):
    """!
            @brief Function that signs user out
    """
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/')
