from django.shortcuts import render


def index(request):
    context = {
        'title': "Notes index page",
        'header': "Notes index page header",
    }
    return render(request, "notes/index.html", context)
