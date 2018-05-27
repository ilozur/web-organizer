from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from main.forms import *
from main.models import *
import json
import hashlib
import binascii
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from morris_butler.settings import SECRET_KEY, EMAIL_HOST_USER, SUPPORTED_LANGUAGES,\
    SUPPORTED_LANGUAGES_CODES, SUPPORTED_TIMEZONES
from calendars.forms import AddingEventForm
from notes.forms import *
from notes.models import *
from todo.models import *
from calendars.models import *
from django.contrib.auth.models import User
from userprofile.forms import RecoverPasswordUserData
from todo.forms import AddTodoForm, EditTodoForm
from localisation import rus, eng
import pytz


def index(request):
    """!
            @brief Function that renders home page if user is authenticated and index page if not
    """
    if request.method == "GET":
        context = {
            'title': 'Index page'
        }
        if not request.user.is_authenticated:
            sign_in_form = SignInForm()
            context['sign_in_form'] = sign_in_form
            sign_up_form = SignUpForm()
            context['sign_up_form'] = sign_up_form
            recover_password_user_data_form = RecoverPasswordUserData()
            context['recover_password_form'] = recover_password_user_data_form
            context['timezones'] = SUPPORTED_TIMEZONES
            context['supported_languages'] = SUPPORTED_LANGUAGES
            return render(request, "main/index.html", context)
        else:
            context['lang'], context['language'] = get_language(request)
            events = Event.objects.filter(user=request.user)
            notes = Notes.objects.filter(user=request.user)
            todos = Todos.objects.filter(user=request.user)
            tzinfo = pytz.timezone(Timezone.objects.filter(user=request.user)[0].timezone)
            date = timezone.now().astimezone(tzinfo)
            today_event = events.filter(date=date.date()).first()
            if today_event:
                context['today_event_exists'] = True
                context['today_event_name'] = today_event.title
                context['today_event_id'] = today_event.id
            context['all_events_count'] = events.count()
            context['today_events_count'] = events.filter(date=date.date()).count()
            context['yesterday_events_count'] = events.filter(date=date.date() - timezone.timedelta(1)).count()
            last_events = events.filter(date__lte=date.date())
            context['week_events_count'] = last_events.filter(date__gte=date.date() - timezone.timedelta(1)).count()
            context['month_events_count'] = last_events.filter(date__gte=date.date() - timezone.timedelta(30)).count()
            context['year_events_count'] = last_events.filter(date__gte=date.date() - timezone.timedelta(365)).count()
            context['all_notes_count'] = notes.count()
            todos_info = Todos.get_amounts(request.user)
            context['all_todo_count'] = todos_info[0]
            context['active_todo_count'] = todos_info[1]
            context['finished_todo_count'] = todos_info[2]
            nearest_events = events.filter(date__gte=date.date()).order_by('date')
            if nearest_events.count() > 0:
                while (nearest_events.first().date == date.date()) and (nearest_events.first().time < date.time()):
                    nearest_events.pop(0)
                    if nearest_events.count() == 0:
                        break
            if nearest_events.first():
                context['nearest_event_exists'] = True
                context['nearest_event_name'] = nearest_events.first().title
                context['nearest_event_place'] = nearest_events.first().place
                context['nearest_event_date'] = nearest_events.first().date.strftime("%d.%m.%Y ") + \
                    nearest_events.first().time.strftime("%H:%M")
            else:
                context['nearest_event_exists'] = False
            nearest_todo = todos.filter(deadline__gte=date.date()).order_by('deadline')
            if nearest_todo.count() > 0:
                while (nearest_todo.first().deadline.date() == date.date()) and\
                        (nearest_todo.first().deadline.time() < date.time()):
                    nearest_todo.pop(0)
                    if nearest_todo.count() == 0:
                        break
            if nearest_todo.first():
                context['nearest_todo_exists'] = True
                context['nearest_todo_name'] = nearest_todo.first().title
            else:
                context['nearest_todo_exists'] = False
            last_note = notes.order_by('-added_time').first()
            if last_note:
                context['last_note_exists'] = True
                context['last_note_title'] = last_note.title
                context['last_note_id'] = last_note.id
            else:
                context['last_note_exists'] = False
            context['add_event_form'] = AddingEventForm()
            context['save_note_form'] = SaveNoteForm()
            context['edit_note_form'] = EditNoteForm()
            context['last_notes'] = get_last_notes(request.user, notes)
            context['last_notes_count'] = len(context['last_notes'])
            context['add_todo_form'] = AddTodoForm()
            context['edit_todo_form'] = EditTodoForm()
            context['hours'] = date.hour
            return render(request, "main/home.html", context)
    else:
        return HttpResponseRedirect('/')


def get_last_notes(user, notes):
    """!
            @brief Function that get last three notes out all
    """
    all_notes = Notes.get_notes("date_up", user, notes)
    if all_notes.count() >= 3:
        first_three = all_notes[0:3]
    else:
        first_three = all_notes
    return first_three


def get_active_todos(user):
    all_todos = Todos.get_todos("date_up", user)
    active_todos = []
    last_active_todos = []
    for item in all_todos:
        if item.status == 'in progress':
            active_todos.append(item)
    if active_todos.count() > 2:
        last_active_todos = active_todos[0:3]
    else:
        last_active_todos = active_todos[0:active_todos.count()]
    return last_active_todos


def get_finished_todos(user):
    all_todos = Todos.get_todos("date_up", user)
    finished_todos = []
    last_finished_todos = []
    for item in all_todos:
        if item.status != 'in progress':
            finished_todos.append(item)
    if finished_todos.count() > 2:
        last_finished_todos = finished_todos[0:3]
    else:
        last_finished_todos = finished_todos[0:finished_todos.count()]
    return last_finished_todos


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
    if request.method == "GET":
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/')
    else:
        response_data = {}
        if not request.user.is_authenticated:
            form = SignUpForm(request.POST)
            language_checker = False
            timezone_checker = False
            if form.is_valid():
                language = form.cleaned_data['language']
                language_checker = language in SUPPORTED_LANGUAGES_CODES
                timezone_name = form.cleaned_data['timezone']
                timezone_checker = timezone_name in SUPPORTED_TIMEZONES
            if form.is_valid() and language_checker and timezone_checker:
                email = form.cleaned_data['email'].lower()
                username = form.cleaned_data['username'].lower()
                name = form.cleaned_data['name']
                surname = form.cleaned_data['surname']
                pass1 = form.cleaned_data['password1']
                pass2 = form.cleaned_data['password2']
                email_uniq = check_email_uniq(email)
                username_uniq = check_username_uniq(username)
                if email_uniq:
                    if username_uniq:
                        if pass1 == pass2:
                            user = User(email=email, username=username, first_name=name, last_name=surname, is_active=0)
                            user.set_password(pass1)
                            user.save()
                            lang = Language(user=user, lang=language)
                            lang.save()
                            timezone = Timezone(user=user, timezone=timezone_name)
                            timezone.save()
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
    tzinfo = pytz.timezone(Timezone.objects.filter(user=user)[0].timezone)
    expiration_date = timezone.now().astimezone(tzinfo).date()
    expiration_date += timezone.timedelta(days=3)
    sign_up_key = ConfirmKey(user=user, key=key, expiration_date=expiration_date)
    return sign_up_key


def activate_key(request, key):
    """!
            @brief Function that activates key if it is valid
    """
    if request.method == "GET":
        keys = ConfirmKey.objects.filter(key=key)
        if keys.count() > 0:
            tzinfo = pytz.timezone(Timezone.objects.filter(user=request.user)[0].timezone)
            if keys.first().expiration_date >= timezone.now().astimezone(tzinfo).date():
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
                name = form.cleaned_data['username_sign_in'].lower()
                password = form.cleaned_data['password']
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


def get_language(request):
    user_lang = Language.objects.filter(user=request.user).first().lang
    if user_lang == "ru":
        lang = rus
    elif user_lang == "en":
        lang = eng
    else:
        lang = eng
    return lang, user_lang
