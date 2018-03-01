from django.shortcuts import render


def index(request):
    context = {
        'title': "Todolist index page",
        'header': "Todolist index page header"
    }
    return render(request, "todolist/index.html", context)
 
 def show_todolist(request, id):
    context = {}
    if request.POST:
        form = ShowTodolistForm(request)
        Todo = Todolist.objects.filter(id=id).first()
        Todolist.data = request.POST['data']
        Todolist.save()
        return HttpResponseRedirect('/todolist')
    else:
        if len(todolist.objects.filter(id=id)) > 0:
            todo = todolist.objects.filter(id=id).first()
            context = {
                'header': "Show note page header",
                'id': id,
                'title': note.name
                'priority' :
                'status':
            }
            form = ShowTodolistForm({'data': todolist.data})
            context['form'] = form
        else:
            context['error'] = True
        return render(request, "notes/show_todolist.html", context)