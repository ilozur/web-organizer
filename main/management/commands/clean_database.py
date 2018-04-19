from django.core.management.base import BaseCommand
from calendars.models import *
from notes.models import *
from todo.models import *
from main.models import Language
from django.contrib.auth.models import User


class Command(BaseCommand):
    args = "There is no args"
    help = 'Cleans database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--notes', '-n',
            help='Should delete all notes',
            action='store_true',
        )
        parser.add_argument(
            '--events', '-e',
            help='Should delete all events',
            action='store_true',
        )
        parser.add_argument(
            '--todo', '-t',
            help='Should delete all todo',
            action='store_true',
        )
        parser.add_argument(
            '--users', '-u',
            help='Should delete all users. Warning! This will delete everything',
            action='store_true',
        )

    def handle(self, *args, **options):
        if options['notes']:
            self.delete_all_notes()
        if options['events']:
            self.delete_all_events()
        if options['todo']:
            self.delete_all_todo()
        if options['users']:
            self.delete_all_users()
        self.stdout.write("Complete!")

    def delete_all_notes(self):
        notes = Notes.objects.all()
        notes_count = notes.count()
        if notes_count == 0:
            return
        counter = 0
        percents = int(counter / notes_count * 100)
        self.stdout.write("Deleting notes: [", ending="")
        for i in range(0, percents):
            self.stdout.write("/", ending="")
        for i in range(0, 100 - percents):
            self.stdout.write("-", ending="")
        self.stdout.write("]")
        for note in notes:
            note.delete()
            counter += 1
            percents = int(counter / notes_count * 100)
            self.stdout.write("Deleting notes: [", ending="")
            for i in range(0, percents):
                self.stdout.write("/", ending="")
            for i in range(0, 100 - percents):
                self.stdout.write("-", ending="")
            self.stdout.write("]")

    def delete_all_events(self):
        events = Event.objects.all()
        events_count = events.count()
        if events_count == 0:
            return
        counter = 0
        percents = int(counter / events_count * 100)
        self.stdout.write("Deleting events: [", ending="")
        for i in range(0, percents):
            self.stdout.write("/", ending="")
        for i in range(0, 100 - percents):
            self.stdout.write("-", ending="")
        self.stdout.write("]")
        for event in events:
            event.delete()
            counter += 1
            percents = int(counter / events_count * 100)
            self.stdout.write("Deleting events: [", ending="")
            for i in range(0, percents):
                self.stdout.write("/", ending="")
            for i in range(0, 100 - percents):
                self.stdout.write("-", ending="")
            self.stdout.write("]")

    def delete_all_users(self):
        self.delete_all_events()
        self.delete_all_notes()
        self.delete_all_todo()
        users = User.objects.all()
        users_count = users.count()
        if users_count == 0:
            return
        counter = 0
        percents = int(counter / users_count * 100)
        self.stdout.write("Deleting users: [", ending="")
        for i in range(0, percents):
            self.stdout.write("/", ending="")
        for i in range(0, 100 - percents):
            self.stdout.write("-", ending="")
        self.stdout.write("]")
        for user in users:
            langs = Language.objects.filter(user=user)
            for lang in langs:
                lang.delete()
            user.delete()
            counter += 1
            percents = int(counter / users_count * 100)
            self.stdout.write("Deleting users: [", ending="")
            for i in range(0, percents):
                self.stdout.write("/", ending="")
            for i in range(0, 100 - percents):
                self.stdout.write("-", ending="")
            self.stdout.write("]")

    def delete_all_todo(self):
        todos = Todos.objects.all()
        todos_count = todos.count()
        if todos_count == 0:
            return
        counter = 0
        percents = int(counter / todos_count * 100)
        self.stdout.write("Deleting todo: [", ending="")
        for i in range(0, percents):
            self.stdout.write("/", ending="")
        for i in range(0, 100 - percents):
            self.stdout.write("-", ending="")
        self.stdout.write("]")
        for todo in todos:
            todo.delete()
            counter += 1
            percents = int(counter / todos_count * 100)
            self.stdout.write("Deleting todo: [", ending="")
            for i in range(0, percents):
                self.stdout.write("/", ending="")
            for i in range(0, 100 - percents):
                self.stdout.write("-", ending="")
            self.stdout.write("]")
