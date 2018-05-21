from django.core.management.base import BaseCommand
from calendars.models import *
from random import choice, randint
from datetime import datetime, timedelta

WORDS = open("/usr/share/dict/words").read().splitlines()


class Command(BaseCommand):
    args = "There is no args"
    help = 'Generates events'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='Events count',
        )
        parser.add_argument(
            '--special-user',
            type=str,
            help='Specifies the user for whom events are generated',
            dest='specified_user',
        )

    def handle(self, *args, **options):
        if options['specified_user']:
            user = User.objects.filter(username=options['specified_user']).first()
            if user:
                self.generate_events(options['count'], user)
            else:
                self.stdout.write("Specified user not found")
        else:
            self.generate_events(options['count'])
        self.stdout.write("Complete!")

    def generate_events(self, count, specified_user=None):
        if specified_user:
            for i in range(0, count):
                self.create_event(specified_user)
                self.stdout.write("Created " + str(i + 1) + " event. Holder: " + specified_user.username)
            self.stdout.write("Successfully generated " + str(count) + " events")
        else:
            for user in User.objects.all():
                for i in range(0, count):
                    self.create_event(user)
                    self.stdout.write("Created " + str(i + 1) + " event. Holder: " + user.username)
            self.stdout.write("Successfully generated " + str(count * User.objects.all().count()) + " events")

    @staticmethod
    def create_event(user):
        text = ' '.join(choice(WORDS) for i in range(randint(10, 50)))
        title = ' '.join(choice(WORDS) for i in range(randint(1, 5)))
        default_date = datetime.now()
        date = default_date.date() + timedelta(randint(0, 365))
        time = (default_date + timedelta(hours=randint(0, 24), minutes=randint(0, 60))).time()
        event = Event(user=user, added_date=datetime.now().date(), added_time=datetime.now().time(),
                      title=title, description=text, is_public=randint(0, 1), date=date, time=time)
        event.save()
