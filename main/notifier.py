from calendars.models import *
from datetime import datetime, timedelta
from main.views import create_mail, send_mail


def notify_if_needed():
    events = Event.objects.all()
    for event in events:
        if not event.notified_already:
            should_notify = check_notify(event)
            if should_notify:
                notify_user(event)


def check_notify(event):
    time_now = datetime.now()
    event_time = datetime(event.date.year, event.date.month, event.date.day,
                          event.time.hour, event.time.minute, event.time.second)
    event_time -= timedelta(days=event.should_notify_days, hours=event.should_notify_hours,
                            minutes=event.should_notify_minutes)
    if event_time < time_now:
        return True
    else:
        return False


def notify_user(event):
    event.notified_already = True
    text = "Dear " + event.user.first_name + " " + event.user.last_name + "! Your event (" + event.title + ") is near!"
    html = "Dear " + event.user.first_name + " " + event.user.last_name + "! Your event (" + event.title + ") is near!"
    mail = create_mail(event.user, text, html)
    send_mail(mail)
    event.save()
