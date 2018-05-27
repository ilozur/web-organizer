from django.db import models
from django.contrib.auth.models import User


class NotesFolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Title")
    recently_deleted = models.BooleanField(default=False)


class Notes(models.Model):
    data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="title")
    added_time = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(NotesFolder, on_delete=models.CASCADE, default=None, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True, default=None)

    @staticmethod
    def get_notes(sorting_type, user=None, notes=None, folder=None):
        """
            @brief
            This function get notes
            @detailed
            This function get notes by time and alphabetically
            if aim = 'date' -> 'up' = new-old, 'down' = old-new
            if aim = 'title' -> 'up' = a-z, 'down' = z-a
            if sorting type is not correct returns returns notes sorted like date_up
        """
        if user is None:
            return None
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
        recently_deleted_folder = NotesFolder.objects.filter(user=user, recently_deleted=True)
        if len(recently_deleted_folder) == 0:
            tmp_folder = NotesFolder(user=user, title="Recently deleted", recently_deleted=True)
            tmp_folder.save()
        recently_deleted_folder = NotesFolder.objects.filter(user=user, recently_deleted=True)
        if folder is None:
            notes = notes.exclude(folder=recently_deleted_folder[0])
        else:
            notes = notes.filter(folder=folder)
        return notes

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
            fully_deleted = False
            if notes[0].folder:
                if notes[0].folder.recently_deleted:
                    notes[0].delete()
                    fully_deleted = True
            if not fully_deleted:
                recently_deleted_folder = NotesFolder.objects.filter(user=user, recently_deleted=True)
                if len(recently_deleted_folder) == 0:
                    tmp_folder = NotesFolder(user=user, title="Recently deleted", recently_deleted=True)
                    tmp_folder.save()
                recently_deleted_folder = NotesFolder.objects.filter(user=user, recently_deleted=True)
                notes[0].folder = recently_deleted_folder[0]
                notes[0].save()
            return 100
        else:
            return 111

    @staticmethod
    def search_notes(aim, user, sorting_type="date_up", folder=None):
        """
        @brief
        This function searches for the notes
        """
        notes = Notes.get_notes(sorting_type, user, folder=folder)
        if aim is None:
            aim = ""
        notes = notes.filter(title__icontains=aim)
        return notes
