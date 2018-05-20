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
    def get_events(sorting_type, user=None):
        """!
            @brief Function that get evens from database by user and sorting type
        """
        # if aim = 'date' -> 'up' = new-old, 'down' = old-new
        # if aim = 'title' -> 'up' = a-z, 'down' = z-a
        sort = sorting_type.split('_')
        aim = sort[0]
        direction = sort[1]
        modificator = sort[2]
        if user:
            events = Event.objects.filter(user=user)
        else:
            events = Event.objects.all()
        if aim == "date":
            if direction == "up":
                events = events.order_by('-date', '-time')
            elif direction == "down":
                events = events.order_by('date', 'time')
        elif aim == "title":
            if direction == "up":
                events = events.order_by('title')
            elif direction == "down":
                events = events.order_by('-title')
        if modificator == 'all':
            pass
        elif modificator == 'public':
            events = events.filter(is_public=1)
        elif modificator == 'private':
            events = events.filter(is_public=0)
        return events

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
        events = events.filter(user=user)
        events = events.filter(date__gte=from_date, date__lte=to_date)
        return events

    @staticmethod
    def get_todo_by_id(id):
        if Event.objects.filter(id=id).count() > 0:
            return Event.objects.filter(id=id).first()
        else:
            return False