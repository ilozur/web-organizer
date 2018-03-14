from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Notes(models.Model):
    data = models.TextField()
    user = models.ForeignKey(User, default=1, on_delete=set([1, ]))
    name = models.CharField(max_length=128, default="title")
    added_time = models.DateTimeField(auto_now_add=True)
    is_voice = models.BooleanField(default=False)

    @staticmethod
    def get_notes(sorting_type, user=1):
        # if aim = 'date' -> 'up' = new-old, 'down' = old-new
        # if aim = 'title' -> 'up' = a-z, 'down' = z-a
        notes = Notes.objects.filter(user=user)
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
        elif aim == "title":
            if direction == "up":
                notes = notes.order_by('name')
            elif direction == "down":
                notes = notes.order_by('-name')
        return notes

    @staticmethod
    def get_note_by_id(id):
        return Notes.objects.filter(id=id).first()

    @staticmethod
    def delete_note(id):
        if len(Notes.objects.filter(id=id)) > 0:
            Notes.objects.filter(id=id).delete()
            return True
        else:
            return False

    @staticmethod
    def search_notes(substr, user):
        obj = Notes.get_notes('all', user)
        ret_list = list()
        for i in obj:
            if substr in i.name:
                ret_list.append((i.name, i.added_time.strftime("%I:%M%p on %B %d, %Y"), i.id))
        return ret_list
