from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Event(models.Model):
    """!
        This is class of user's events
    """
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    added_date = models.DateField(default="2018-01-01")
    added_time = models.TimeField(default="00:00:00:000000")
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_public = models.BooleanField()
    date = models.DateField(default="2018-01-01")
    time = models.TimeField()
    status = models.CharField(max_length=64, default="opened")
    notified_already = models.BooleanField(default=False)
    should_notify_hours = models.SmallIntegerField(default=0)
    should_notify_minutes = models.SmallIntegerField(default=0)
    should_notify_days = models.SmallIntegerField(default=0)
    place = models.CharField(max_length=255, default="none")

    @staticmethod
    def get_events(sorting_type, user, modifier=1):
        """!
            @brief Function that get evens from database by user and sorting type
        """
        mode = {
            'AtoZ': 'title',
            'ZtoA': '-title',
            'old': ('-date', '-time'),
            'new': ('date', 'time')
        }
        events_list = list()
        events = Event.objects.order_by(mode.get(sorting_type))
        if modifier == 0:
            events = events.filter(user=user)
        else:
            events = events.exclude(is_public=modifier) | events.filter(user=user, is_public=modifier)
        for item in events:
            events_list.append((item.title, item.date, item.id, item.description, item.place))
        return events_list

    @staticmethod
    def get_event_by_id(id):
        if Event.objects.filter(id=id).exists():
            return Event.objects.filter(id=id).first()
        else:
            return False

    @staticmethod
    def delete_event(event_id):
        """!
            @brief This function delete event from DB by id, if id is valid
        """
        if len(Event.objects.filter(id=event_id)) > 0:
            Event.objects.filter(id=event_id).delete()
            return True
        else:
            return False

    @staticmethod
    def get_events_in_range(from_date, to_date, user, events=None):
        """!
            @brief This function get list of events by user and diapason of dates
        """
        if events is None:
            events = Event.objects.all()
        events_list = list()
        events = events.filter(user=user, date__gte=from_date, date__lte=to_date)
        for item in events:
            events_list.append((item.title, item.date, item.id, item.description, item.place))
        return events

    @staticmethod
    def get_todo_by_id(id):
        if Event.objects.filter(id=id).count() > 0:
            return Event.objects.filter(id=id).first()
        else:
            return False