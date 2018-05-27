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

    def handle(self, *args, **options):
        if User.objects.filter(username=options['username']).count() > 0:
            User.objects.filter(username=options['username'])[0].delete()
            self.stdout.write("User was successfully deleted")
        else:
            if options['email']:
                if User.objects.filter(email=options['email']).count() > 0:
                    User.objects.filter(email=options['email'])[0].delete()
                    self.stdout.write("User was successfully deleted")
                else:
                    self.stdout.write("User not found")
            else:
                self.stdout.write("User not found")

    @staticmethod
    def create_user(username, password, language, email="", timezone=None):
        user = User(username=username, email=email, is_active=True)
        user.set_password(password)
        user.save()
        lang = Language(user=user, lang=language)
        lang.save()
        if timezone is None:
            timezone = TIME_ZONE
        tmp_timezone = Timezone(user=user, timezone=timezone)
        tmp_timezone.save()
