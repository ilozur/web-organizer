from django.shortcuts import render


def index(request):
    context = {
        'title': "Index page",
        'header': "Index page header",
    }
    return render(request, "main/index.html", context)
