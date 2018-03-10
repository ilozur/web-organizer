from django.core.management.base import BaseCommand
from calendars.models import *
from datetime import datetime, timedelta
from main.views import create_mail, send_mail


class Command(BaseCommand):
    args = "There is no args"
    help = 'Notifies all users'

    def handle(self, *args, **options):
        Command.notify_if_needed(self)
        self.stdout.write("Complete!")

    def notify_if_needed(self):
        events = Event.objects.all()
        for event in events:
            if not event.notified_already:
                should_notify = Command.check_notify(event)
                if should_notify:
                    Command.notify_user(event)
                    self.stdout.write("Successfully notified " + event.user.username + " user")

    @staticmethod
    def check_notify(event):
        time_now = datetime.now()
        event_time = datetime(event.date.year, event.date.month, event.date.day,
                              event.time.hour, event.time.minute, event.time.second)
        event_time -= timedelta(days=event.should_notify_days, hours=event.should_notify_hours,
                                minutes=event.should_notify_minutes)
        if event_time <= time_now:
            return True
        else:
            return False

    @staticmethod
    def notify_user(event):
        event.notified_already = True
        text = "Dear " + event.user.first_name + " " + event.user.last_name +\
               "! Your event (" + event.title + ") is near!"
        html = "Dear " + event.user.first_name + " " + event.user.last_name +\
               "! Your event (" + event.title + ") is near!"
        mail = create_mail(event.user, text, html)
        send_mail(mail)
        event.save()
