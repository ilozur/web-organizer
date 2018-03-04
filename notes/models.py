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
    def get_notes_by_ranged_name(user, name_range=[]):
        notes = Notes.objects.filter(user=user)
        sorted_list = []
        if len(name_range) == 1:
            for i in notes:
                if i.name[0] == name_range.lower():
                    sorted_list.append(i)
        else:
            for i in notes:
                if name_range[0] <= i.name[0] <= name_range[1]:
                    sorted_list.append(i)
        return sorted_list



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
