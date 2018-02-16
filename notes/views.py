from django.shortcuts import render

def index(request):
    context = {
        'title': "Notes index page",
        'header': "Notes index page header",
    }
    return render(request, "notes/index.html", context)

def add_note(request):
    context = {
        'header': "Add_note page"
    }
    return render(request, "notes/add_note.html", context)
