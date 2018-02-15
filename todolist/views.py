from django.shortcuts import render


def index(request):
    context = {
        'title': "Todolist index page",
        'header': "Todolist index page header"
    }
    return render(request, "todolist/index.html", context)

def add_todo():
    pass