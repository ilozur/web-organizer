from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Event(models.Model):
    """!
        @brief This is class of user's events.
    """

    ##@brief This variable contain number of user who create this event.
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))

    ##@brief This variable contain date of adding event.
    added_date = models.DateField(default="2018-01-01")

    ##@brief This variable contain time of adding.
    added_time = models.TimeField(default="00:00:00:000000")

    ##@brief This variable contain title.
    title = models.CharField(max_length=255)

    ##@brief This variable contain description.
    description = models.TextField()

    ##@brief This variable contain informations about is an public this variable or not.
    is_public = models.BooleanField()

    ##@brief This variable contain date why this event will happen.
    date = models.DateField(default="2018-01-01")

    ##@brief This variable contain time why event will happen.
    time = models.TimeField()

    ##@brief This field contain information about stage of progress of event.
    status = models.CharField(max_length=64, default="opened")

    ##@brief This variable contain information about sending notification to email (can be true or false).
    notified_already = models.BooleanField(default=False)

    ##@brief This variable contain information about time (hour) why notification will be send.
    should_notify_hours = models.SmallIntegerField(default=0)

    ##@brief This variable contain information about time (minute) why notification will be send.
    should_notify_minutes = models.SmallIntegerField(default=0)

    ##@brief This variable contain information about date why notification will be send.
    should_notify_days = models.SmallIntegerField(default=0)

    ##@brief This fiels contain name of place where event will happen.
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
