from django.shortcuts import render


def index(request):
    context = {
        'title': "Todo index page",
        'header': "Todo index page header"
    }
    return render(request, "todo/index.html", context)
