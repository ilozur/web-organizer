from django.core.management.base import BaseCommand
from calendars.models import *
from random import choice, randint
from string import ascii_letters
from main.models import Language


class Command(BaseCommand):
    args = "There is no args"
    help = 'Generates users with " " password'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='Users count',
        )

    def handle(self, *args, **options):
        self.generate_users(options['count'])
        self.stdout.write("Complete!")

    def generate_users(self, count):
        for i in range(0, count):
            self.create_user()

    def create_user(self):
        username = ''.join(choice(ascii_letters) for i in range(randint(10, 25)))
        if User.objects.filter(username=username).count() == 0:
            user = User(username=username, is_active=True)
            user.set_password(" ")
            user.save()
            tmp = ['ru', 'en']
            lang = Language(user=user, lang=choice(tmp))
            lang.save()
            result = "ok"
        else:
            result = "username used"
        if result == "ok":
            self.stdout.write("User was successfully created: " + username)
        elif result == "username used":
            self.stdout.write("Username has already used")
