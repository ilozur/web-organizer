from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Language, Timezone
from morris_butler.settings import TIME_ZONE, SUPPORTED_TIMEZONES, SUPPORTED_LANGUAGES_CODES


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
        parser.add_argument(
            'language',
            type=str,
            help='Language("ru" and "en" are supported)',
        )
        parser.add_argument(
            '--timezone',
            type=str,
            help='Timezone',
            dest='timezone',
        )

    def handle(self, *args, **options):
        timezone = options['timezone']
        if timezone:
            if timezone not in SUPPORTED_TIMEZONES:
                timezone = None
        if User.objects.filter(username=options['username']).count() == 0:
            if options['email']:
                if User.objects.filter(email=options['email']).count() == 0:
                    self.create_user(options['username'], options['password'], options['language'],
                                     options['email'], timezone=timezone)
                    self.stdout.write("User was successfully created")
                else:
                    self.stdout.write("Email has already used")
            else:
                self.create_user(options['username'], options['password'], options['language'], timezone=timezone)
                self.stdout.write("User was successfully created")
        else:
            self.stdout.write("Username has already used")

    @staticmethod
    def create_user(username, password, language, email="", timezone=None):
        user = User(username=username, email=email, is_active=True)
        user.set_password(password)
        user.save()
        if not language in SUPPORTED_LANGUAGES_CODES:
            language = "en"
        lang = Language(user=user, lang=language)
        lang.save()
        if timezone is None:
            timezone = TIME_ZONE
        elif timezone not in SUPPORTED_TIMEZONES:
            timezone = TIME_ZONE
        tmp_timezone = Timezone(user=user, timezone=timezone)
        tmp_timezone.save()
