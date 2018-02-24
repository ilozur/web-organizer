from django.http import HttpResponseRedirect
from django.shortcuts import render
from notes.forms import AddNoteForm, SearchForm, ShowNoteForm
from notes.models import Notes


def index(request):
    context = {
        'title': "Notes index page",
        'header': "Notes index page header",
    }
    notes_list = list()
    notes = get_notes('title_up', 1)
    for i in notes:
        notes_list.append((i.name, i.added_time, i.id))
    context['notes_data'] = notes_list
    search_form = SearchForm()
    context['search_form'] = search_form
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


def search(substr):
    obj = Notes.objects.all()
    ret_list = []
    for i in obj:
        if substr in i.name:
            ret_list.append(i)

    return ret_list


def show_note(request, id):
    context = {}
    if request.POST:
        form = ShowNoteForm(request)
        note = Notes.objects.filter(id=id).first()
        note.data = request.POST['data']
        note.save()
        return HttpResponseRedirect('/notes')
    else:
        if len(Notes.objects.filter(id=id)) > 0:
            note = Notes.objects.filter(id=id).first()
            context = {
                'header': "Show note page header",
                'id': id,
                'title': note.name
            }
            form = ShowNoteForm({'data': note.data})
            context['form'] = form
        else:
            context['error'] = True
        return render(request, "notes/show_note.html", context)


def get_notes(sorting_type, user=1):
    # if aim = 'date' -> 'up' = new-old, 'down' = old-new
    # if aim = 'title' -> 'up' = a-z, 'down' = z-a
    sort = sorting_type.split('_')
    aim = sort[0]
    direction = sort[1]
    notes = Notes.objects.filter(user=user)
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
