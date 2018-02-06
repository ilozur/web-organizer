from django.shortcuts import render


def index(request):
    context = {
        'title': "Calendar index page",
        'header': "Calendar index page header",
    }
    return render(request, "calendars/index.html", context)
