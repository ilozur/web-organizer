from datetime import datetime
import socket

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from threading import Thread

from main.forms import SignInForm, SignUpForm
from main.models import Language
from main.views import check_email_uniq, check_username_uniq, create_unic_key, create_mail, send_mail
from notes.forms import AddNoteForm, EditNoteForm
from notes.models import Notes


class Logger:
    path = ""
    f = None

    @staticmethod
    def prepare_logger(path):
        Logger.path = path

    @staticmethod
    def save_logs(logs):
        Logger.f = open(Logger.path, 'a')
        Logger.f.write(logs + '\n')
        Logger.f.close()


class Listening(Thread):
    def __init__(self, name, ip, port):
        Thread.__init__(self)
        self.user = name
        self.port = port
        self.ip = ip
        self.sock = None

    def run(self):
        self.sock = socket.socket()
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        while True:
            conn, addr = self.sock.accept()
            Logger.save_logs('Connected: ' + addr[0] + " (" + str(datetime.now()) + ")")
            bytes_data = conn.recv(1024)
            if bytes_data:
                data = bytes_data.decode('utf-8')
                cmds = data.split('||')
                if len(cmds) >= 3:
                    if cmds[0] == "login":
                        form = SignInForm({'password': cmds[2], 'username_sign_in': cmds[1]})
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
                                    loginned_user = authenticate(username=user.username, password=password)
                                    if loginned_user is None:
                                        result = "107"
                                    else:
                                        print(loginned_user.username)
                                        userthread = ListeningUser(loginned_user.username, conn, addr)
                                        userthread.daemon = True
                                        userthread.start()
                                        result = "100"
                                else:
                                    result = "108"
                        else:
                            result = "104"
                        conn.send(result.encode())
                        if result != "100":
                            conn.close()
                    elif cmds[0] == "register":
                        form = SignUpForm(
                            {'username': cmds[1], 'password1': cmds[2], 'password2': cmds[2], 'email': cmds[3],
                             'name': cmds[4], 'surname': cmds[5]})
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
                                        user = User(email=email, username=username, first_name=name, last_name=surname,
                                                    is_active=0)
                                        user.set_password(pass1)
                                        user.save()
                                        # here should be lang=*lang taken from registration*
                                        lang = Language(user=user)
                                        lang.save()
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
                        conn.send(result.encode())
                        conn.close()
                    else:
                        result = "105"
                        conn.send(result.encode())
                        conn.close()


class ListeningUser(Thread):
    def __init__(self, name, conn, addr):
        Thread.__init__(self)
        self.user = User.objects.filter(username=name).first()
        self.conn = conn
        self.addr = addr

    def run(self):
        Logger.save_logs("Started private connection with user " + self.addr[0] +
                         " (" + str(datetime.now()) + ")")
        while True:
            try:
                bytes_data = self.conn.recv(1024)
            except ConnectionResetError:
                self.conn.close()
            if bytes_data:
                data = bytes_data.decode('utf-8')
                cmds = data.split('||')
                if cmds[0] == "add_note":
                    self.add_note(cmds)
                if cmds[0] == "get_all_notes":
                    self.get_all_notes()
                if cmds[0] == "get_note":
                    self.get_note(cmds[1])
                    # speaking commands with user

    def add_note(self, cmds):
        form = AddNoteForm({'note_title': cmds[1], 'note_data': cmds[2], 'note_data_part': cmds[2]})
        if form.is_valid():
            name = form.cleaned_data['note_title']
            data = form.cleaned_data['note_data']
            data_part = form.cleaned_data['note_data_part']
            tmp = Notes(name=name, data=data, added_time=datetime.now(),
                        user=User.objects.filter(username=self.user).first(), data_part=data_part)
            tmp.save()
            result = "100"
        else:
            result = '104'
        self.conn.send(result.encode())

    def get_all_notes(self):
        result = "100"
        notes_list = Notes.objects.filter(user=self.user)
        for i in notes_list:
            result += '|' + str(i.id)
        self.conn.send(result.encode())

    def get_note(self, id):
        note = Notes.objects.filter(user=self.user, id=id).first()
        result = '100|' + note.name + '|' + note.data
        self.conn.send(result.encode())

    def edit_note(self, cmds):
        form = EditNoteForm({'note_title_edit': cmds[1], 'note_data_edit': cmds[2], 'note_id': cmds[2]})
        if form.is_valid():
            note_id = form.cleaned_data['note_id']
            if Notes.objects.filter(user=request.user, id=note_id).count() > 0:
                tmp = Notes.objects.filter(id=note_id).first()
                tmp.name = form.cleaned_data['note_title_edit']
                tmp.data = form.cleaned_data['note_data_edit']
                tmp.data_part = form.cleaned_data['note_data_part_edit']
                tmp.last_edit_time = datetime.now()
                tmp.save()
                result = '100'
            else:
                result = '111'
        else:
            result = '104'
        self.conn.send(result.encode())



class Command(BaseCommand):
    args = "There is no args"
    help = "Starts the api server"

    def add_arguments(self, parser):
        parser.add_argument(
            'ip',
            type=str,
            help='Server ip',
        )
        parser.add_argument(
            'port',
            type=int,
            help='Server port',
        )

    def handle(self, *args, **options):
        Logger.prepare_logger("logs.txt")
        self.start_server(options['ip'], options['port'])
        while True:
            cmd = input("> ")
            if cmd == "exit":
                exit()

    def start_server(self, ip, port):
        self.stdout.write("Starting server on " + ip + ":" + str(port))
        Logger.save_logs("Starting server on " + ip + ":" + str(port) + " (" + str(datetime.now()) + ")")
        try:
            listening_thread = Listening("authentication_server", ip, port)
            listening_thread.daemon = True
            listening_thread.start()
            Logger.save_logs("Server successfully has started! (" + str(datetime.now()) + ")")
            self.stdout.write("Server successfully has started!")
        except OSError:
            print("Error! Restart the server")
            Logger.save_logs("Error!")
            exit()
