from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
    data = models.TextField()
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    title = models.CharField(max_length=50, default="title")
    added_time = models.DateTimeField(auto_now_add=True)
    last_edit_time = models.DateTimeField(default=None, null=True)

    @staticmethod
    def get_notes_by_ranged_title(user, title_range=list()):
        """
        @brief
        This function get notes by ranged title
        """
        notes = Notes.objects.filter(user=user)
        sorted_list = []
        if len(title_range) == 1:
            for i in notes:
                if i.title[0].lower() == title_range[0].lower():
                    sorted_list.append(i)
        else:
            for i in notes:
                if title_range[0].lower() <= i.title[0].lower() <= title_range[1].lower():
                    sorted_list.append(i)
        return sorted_list

    @staticmethod
    def get_notes(sorting_type, user=1, notes=None):
        """
            @brief
            This function get notes
            @detailed
            This function get notes by time and alphabetically
            if aim = 'date' -> 'up' = new-old, 'down' = old-new
            if aim = 'title' -> 'up' = a-z, 'down' = z-a
            if sorting type is not correct returns returns notes sorted like date_up
        """
        if notes is None:
            notes = Notes.objects.filter(user=user)
        notes = notes.filter(user=user).order_by('-added_time')
        sorting_types = ['date_up', 'date_down', 'title_up', 'title_down', 'all']
        if sorting_type not in sorting_types:
            sorting_type = "date_up"
        if sorting_type != 'all':
            sort = sorting_type.split('_')
            aim = sort[0]
            direction = sort[1]
        else:
            return notes
        if aim == "date":
            if direction == "up":
                notes = notes.order_by('-added_time')
            elif direction == "down":
                notes = notes.order_by('added_time')
            else:
                return notes
        elif aim == "title":
            if direction == "up":
                notes = notes.order_by('title')
            elif direction == "down":
                notes = notes.order_by('-title')
            else:
                return notes
        else:
            return notes
        return notes

    @staticmethod
    def get_note_by_id(note_id):
        """
        @param
        This is ID of notes
        @brief
        This function gets note by id
        """
        return Notes.objects.filter(id=note_id).first()

    @staticmethod
    def delete_note(note_id, user):
        """
        @param
        This is ID of notes
        @brief
        This function deletes note
        """
        notes = Notes.objects.filter(user=user, id=note_id)
        if len(notes) > 0:
            notes[0].delete()
            return 100
        else:
            return 111

    @staticmethod
    def search_notes(string, user, sorting_type="date_up"):
        """
        @brief
        This function searches for the notes
        """
        obj = Notes.get_notes(sorting_type, user)
        ret_list = list()
        for i in obj:
            if string in i.title:
                ret_list.append(i)
        return ret_list

    @staticmethod
    def notes_sort_by_date(datetime, user):  # note: datetime = {1: date_one NOT NULL, 2: date_two}
        """
        @param
        This is the time at which the notes are sorted
        @brief
        This function sorts notes
        @detailed
        This function sorts notes by date and alphabetically and aslo from new to old and conversely
        """
        notelist = Notes.objects.filter(user=user)
        if len(datetime) == 1:
            date = datetime[0].date()
            return notelist.filter(pub_date=date)
        else:
            return notelist.filter(pub_date__gte=datetime[0].date(),
                                   pub_date__lte=datetime[1].date()).order_by('-pub_date')
