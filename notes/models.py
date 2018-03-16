from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Notes(models.Model):
    data = models.TextField()
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    name = models.CharField(max_length=128, default="title")
    added_time = models.DateTimeField(auto_now_add=True)
    is_voice = models.BooleanField(default=False)
    last_edit_time = models.DateTimeField(default=None)

    @staticmethod
    def get_notes_by_ranged_name(user, name_range=list()):
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
    def get_notes ( sorting_type, user=1 ):
        # if aim = 'date' -> 'up' = new-old, 'down' = old-new
        # if aim = 'title' -> 'up' = a-z, 'down' = z-a
        notes = Notes.objects.filter ( user=user )
        if sorting_type != 'all':
            sort = sorting_type.split ( '_' )
            aim = sort[0]
            direction = sort[1]
        else:
            return notes
        if aim == "date":
            if direction == "up":
                notes = notes.order_by ( '-added_time' )
            elif direction == "down":
                notes = notes.order_by ( 'added_time' )
        elif aim == "title":
            if direction == "up":
                notes = notes.order_by ( 'name' )
            elif direction == "down":
                notes = notes.order_by ( '-name' )
        return notes

    @staticmethod
    def get_note_by_id(note_id):
        return Notes.objects.filter(id=note_id).first()

    @staticmethod
    def delete_note(id):
        if len(Notes.objects.filter(id=id)) > 0:
            Notes.objects.filter(id=id).delete()
            return True
        else:
            return False

    @staticmethod
    def search_notes(string, user):
        obj = Notes.get_notes('all', user)
        ret_list = list()
        for i in obj:
            if string in i.name:
                ret_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id))
        return ret_list

    @staticmethod
    def notes_sort_by_date(datetime, user):  # note: datetime = {1: date_one NOT NULL, 2: date_two}
        notelist = Notes.objects.filter(user=user)
        if len(datetime) == 1:
            date = datetime[0].date()
            return notelist.filter(pub_date=date)
        else:
            return notelist.filter(pub_date__gte=datetime[0].date(),
                                   pub_date__lte=datetime[1].date()).order_by('-pub_date')

