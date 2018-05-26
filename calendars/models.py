from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta


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
            'old': '-date',
            'new': 'date'
        }
        events_list = list()
        events = Event.objects.order_by(mode.get(sorting_type))
        if modifier == 0:
            events = events.filter(user=user)
        else:
            events = events.exclude(is_public=modifier) | events.filter(user=user, is_public=modifier)
        for item in events:
            events_list.append((item.title, item.date.strftime("%B %d, %Y"), item.id, item.description, item.place))
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
            events = Event.objects.filter(user=user)
        events_list = list()
        events = events.filter(user=user, date__gte=from_date, date__lte=to_date)
        for item in events:
            events_list.append((item.title, item.date, item.id, item.description, item.place))
        return events

    @staticmethod
    def get_event_by_id(id):
        if Event.objects.filter(id=id).count() > 0:
            return Event.objects.filter(id=id).first()
        else:
            return False

    @staticmethod
    def week_events(sort_type, user):
        mode = {
            'AtoZ': 'title',
            'ZtoA': '-title',
            'old': '-date',
            'new': 'date'
        }
        today = datetime.today()
        weekend = 7 - datetime.weekday(today)
        result = Event.get_events_in_range(today, today + timedelta(weekend), user)
        result = result.order_by(mode.get(sort_type))
        events = list()
        for item in result:
            events.append((item.title, item.date.strftime("%B %d, %Y"), item.id, item.description, item.place))
        return events

    @staticmethod
    def get_weeks(date_time, events):
        """!
            @brief This function select weeks and belong them events
        """
        date = date_time
        datetime_now = datetime.now()
        if (date.month == datetime_now.month) and (date.year == datetime_now.year):
            now_month = True
        else:
            now_month = False
        date -= timedelta(days=date.weekday())
        if (date.day > 1) and (date.month == date_time.month):
            date -= timedelta(days=7 * (date.day // 7))
            if date.month == date_time.month:
                date -= timedelta(days=7)
        weeks = []
        for i in range(1, 5):
            tmp = dict()
            tmp['week_num'] = i
            week_days = []
            for day in range(1, 8):
                tmp_day = dict()
                tmp_day['day'] = date.day
                day_class = ""
                if now_month:
                    if (date.day == date_time.day) and (date.month == date_time.month):
                        day_class = "today"
                    elif date.month != date_time.month:
                        day_class = "future-date"
                else:
                    if date.month != date_time.month:
                        day_class = "future-date"
                tmp_day_events = events.filter(date=date)
                tmp_day['class'] = day_class
                if tmp_day_events.count() > 0:
                    tmp_day['event'] = {'caption': tmp_day_events[0].title, 'id': tmp_day_events[0].id}
                week_days.append(tmp_day)
                date += timedelta(days=1)
            tmp['week_days'] = week_days
            weeks.append(tmp)
        last_month = date.month
        while last_month == date.month:
            tmp = dict()
            tmp['week_num'] = len(weeks) + 1
            week_days = []
            for day in range(1, 8):
                tmp_day = dict()
                tmp_day['day'] = date.day
                day_class = ""
                if now_month:
                    if (date.day == date_time.day) and (date.month == date_time.month):
                        day_class = "today"
                    elif date.month != date_time.month:
                        day_class = "future-date"
                else:
                    if date.month != date_time.month:
                        day_class = "future-date"
                tmp_day['class'] = day_class
                tmp_day_events = events.filter(date=date)
                if tmp_day_events.count() > 0:
                    tmp_day['event'] = {'caption': tmp_day_events[0].title, 'id': tmp_day_events[0].id}
                week_days.append(tmp_day)
                date += timedelta(days=1)
            tmp['week_days'] = week_days
            weeks.append(tmp)
        return weeks

    @staticmethod
    def get_month_name(month):
        """!
            @brief This functon get name of month by number
        """
        m = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
             "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь", ]
        return m[month - 1]

    @staticmethod
    def get_stats(date, user):
        queryset = Event.objects.filter(user=user)
        all_events = queryset.count()
        today = queryset.filter(date=date.date()).count()
        yesterday = queryset.filter(date=date.date() - timedelta(1)).count()
        last_events = queryset.filter(date__lte=date.date())
        weekly = last_events.filter(date__gte=date.date() - timedelta(1)).count()
        monthly = last_events.filter(date__gte=date.date() - timedelta(30)).count()
        yearly = last_events.filter(date__gte=date.date() - timedelta(365)).count()
        return [all_events, today, yesterday, weekly, monthly, yearly]
