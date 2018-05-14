from django.core.management.base import BaseCommand
from notes.models import *
from random import choice, randint
from string import ascii_letters
from datetime import datetime


class Command(BaseCommand):
    args = "There is no args"
    help = 'Generates notes'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='Notes count',
        )
        parser.add_argument(
            '--special-user',
            type=str,
            help='Specifies the user for whom notes are generated',
            dest='specified_user',
        )

    def handle(self, *args, **options):
        if options['specified_user']:
            user = User.objects.filter(username=options['specified_user']).first()
            if user:
                self.generate_notes(options['count'], user)
            else:
                self.stdout.write("Specified user not found")
        else:
            self.generate_notes(options['count'])
        self.stdout.write("Complete!")

    def generate_notes(self, count, specified_user=None):
        if specified_user:
            for i in range(0, count):
                self.create_note(specified_user)
                self.stdout.write("Created " + str(i + 1) + " note. Holder: " + specified_user.username)
            self.stdout.write("Successfully generated " + str(count) + " notes")
        else:
            for user in User.objects.all():
                for i in range(0, count):
                    self.create_note(user)
                    self.stdout.write("Created " + str(i + 1) + " note. Holder: " + user.username)
            self.stdout.write("Successfully generated " + str(count * User.objects.all().count()) + " notes")

    @staticmethod
    def create_note(user):
        text = ''.join(choice(ascii_letters) for i in range(randint(10, 500)))
        title = ''.join(choice(ascii_letters) for i in range(randint(10, 50)))
        note = Notes(user=user, data=text, name=title, added_time=datetime.now(), data_part=text[0:255:])
        note.save()
