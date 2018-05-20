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
    def get_weeks(date_time, user, events):
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


    def get_month_name(month):
        """!
            @brief This functon get name of month by number
        """
        m = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
             "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь", ]
        return m[month - 1]



    def create_calendar_statistics(request):
        exit_data = {}
        date = datetime.now()
        events = Event.objects.filter(user=request.user)
        exit_data['weeks'] = Event.get_weeks(date, request.user, events)
        exit_data['all_events_count'] = events.count()
        exit_data['today_events_count'] = events.filter(date=date.date()).count()
        exit_data['yesterday_events_count'] = events.filter(date=date.date() - timedelta(1)).count()
        exit_data['week_events_count'] = last_events = events.filter(date__lte=date.date())
        exit_data['week_events_count'] = last_events.filter(date__gte=date.date() - timedelta(1)).count()
        exit_data['month_events_count'] = last_events.filter(date__gte=date.date() - timedelta(30)).count()
        exit_data['year_events_count'] = last_events.filter(date__gte=date.date() - timedelta(365)).count()
        exit_data['now_month'] = Event.get_month_name(date.month)
        exit_data['now_year'] = date.year
        exit_data['now_month_num'] = date.month
        exit_data['now_date'] = str(date.year) + "_" + str(date.month)
        return exit_data