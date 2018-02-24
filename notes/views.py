from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.forms import AddNoteForm
from notes.models import Notes


def index(request):
    context = {
        'title': "Notes index page",
        'header': "Notes index page header",
    }
    notes_list = list()
    for i in Notes.objects.filter(id=1):
        notes_list.append((i.name, i.added_time, i.id))
    context['notes_data'] = notes_list
    return render(request, "notes/index.html", context)


def add_note(request):
    if request.POST:
        form = AddNoteForm(request.POST)
        tmp_note = Notes(name=form.data['title'], data=form.data['data'])
        tmp_note.save()
        return HttpResponseRedirect('/notes')
    else:
        context = {
            'header': "Add_note page"
        }
        form = AddNoteForm()
        context['form'] = form
        return render(request, "notes/add_note.html", context)
