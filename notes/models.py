from django.db import models
from django.contrib.auth.models import User


class Notes(models.Model):
    data = models.TextField()
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    name = models.CharField(max_length=128, default="title")
    added_time = models.DateTimeField(auto_now_add=True)
    is_voice = models.BooleanField(default=False)
    data_part = models.TextField(max_length=128, default="...")
    last_edit_time = models.DateTimeField(default=None, null=True)

    @staticmethod
    def get_notes_by_ranged_name(user, name_range=list()):
        """
        @brief
        This function get notes by ranged_name
        """
        notes = Notes.objects.filter(user=user)
        sorted_list = []
        if len(name_range) == 1:
            for i in notes:
                if i.name[0].lower() == name_range[0].lower():
                    sorted_list.append(i)
        else:
            for i in notes:
                if name_range[0].lower() <= i.name[0].lower() <= name_range[1].lower():
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
                notes = notes.order_by('name')
            elif direction == "down":
                notes = notes.order_by('-name')
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
    def delete_note(note_id):
        """
        @param
        This is ID of notes
        @brief
        This function deletes note
        """
        if len(Notes.objects.filter(id=note_id)) > 0:
            Notes.objects.filter(id=note_id).delete()
            return True
        else:
            return False

    @staticmethod
    def search_notes(string, user):
        """
        @brief
        This function serches for the notes
        """
        obj = Notes.get_notes('all', user)
        ret_list = list()
        for i in obj:
            if string in i.name:
                ret_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id))
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
