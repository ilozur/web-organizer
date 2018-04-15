from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    args = "There is no args"
    help = 'Creates user'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='Username',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email',
            dest='email',
        )
        parser.add_argument(
            'password',
            type=str,
            help='Password',
        )

    def handle(self, *args, **options):
        if User.objects.filter(username=options['username']).count() == 0:
            if options['email']:
                if User.objects.filter(email=options['email']).count() == 0:
                    self.create_user(options['username'], options['password'], options['email'])
                    self.stdout.write("User was successfully created")
                else:
                    self.stdout.write("Email has already used")
            else:
                self.create_user(options['username'], options['password'])
                self.stdout.write("User was successfully created")
        else:
            self.stdout.write("Username has already used")

    @staticmethod
    def create_user(username, password, email=""):
        user = User(username=username, email=email, is_active=True)
        user.set_password(password)
        user.save()
