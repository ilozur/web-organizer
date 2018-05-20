from django.core.management.base import BaseCommand
from todo.models import *
from random import choice, randint
from string import ascii_letters


class Command(BaseCommand):
    args = "There is no args"
    help = 'Generates todo'

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='Todo count',
        )
        parser.add_argument(
            '--special-user',
            type=str,
            help='Specifies the user for whom todo are generated',
            dest='specified_user',
        )

    def handle(self, *args, **options):
        if options['specified_user']:
            user = User.objects.filter(username=options['specified_user']).first()
            if user:
                self.generate_todo(options['count'], user)
            else:
                self.stdout.write("Specified user not found")
        else:
            self.generate_todo(options['count'])
        self.stdout.write("Complete!")

    def generate_todo(self, count, specified_user=None):
        if specified_user:
            for i in range(0, count):
                self.create_todo(specified_user)
                self.stdout.write("Created " + str(i + 1) + " todo. Holder: " + specified_user.username)
            self.stdout.write("Successfully generated " + str(count) + " todo")
        else:
            for user in User.objects.all():
                for i in range(0, count):
                    self.create_todo(user)
                    self.stdout.write("Created " + str(i + 1) + " todo. Holder: " + user.username)
            self.stdout.write("Successfully generated " + str(count * User.objects.all().count()) + " todo")

    @staticmethod
    def create_todo(user):
        title = ''.join(choice(ascii_letters) for i in range(randint(10, 50)))
        todo = Todos(user=user, title=title)
        todo.save()
