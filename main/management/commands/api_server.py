import socket
import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from threading import Thread
from main.forms import *


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
        self.name = name
        self.port = port
        self.ip = ip
        self.sock = None

    def run(self):
        self.sock = socket.socket()
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        while True:
            conn, addr = self.sock.accept()
            Logger.save_logs('Connected: ' + addr[0] + " (" + str(datetime.datetime.now()) + ")")
            bytes_data = conn.recv(1024)
            if bytes_data:
                data = bytes_data.decode('utf-8')
                cmds = data.split('||')
                if len(cmds) >= 3:
                    if cmds[0] == "login":
                        form = SignInForm({'password': cmds[1], 'username_sign_in': cmds[2]})
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


class ListeningUser(Thread):
    def __init__(self, name, conn, addr):
        Thread.__init__(self)
        self.name = name
        self.conn = conn
        self.addr = addr

    def run(self):
        Logger.save_logs("Started private connection with user " + self.addr[0] +
                         " (" + str(datetime.datetime.now()) + ")")
        while True:
            bytes_data = self.conn.recv(1024)
            if bytes_data:
                data = bytes_data.decode('utf-8')
                self.conn.send("OK".encode())
                # speaking commands with user


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
        Logger.save_logs("Starting server on " + ip + ":" + str(port) + " (" + str(datetime.datetime.now()) + ")")
        try:
            listening_thread = Listening("authentication_server", ip, port)
            listening_thread.daemon = True
            listening_thread.start()
            Logger.save_logs("Server successfully has started! (" + str(datetime.datetime.now()) + ")")
            self.stdout.write("Server successfully has started!")
        except OSError:
            print("Error! Restart the server")
            Logger.save_logs("Error!")
            exit()
