from django.shortcuts import render


def index(request):
    context = {
        'title': "Todolist index page",
        'header': "Todolist index page header"
    }
    return render(request, "todolist/index.html", context)
 
 def edit_todolist(request, id):
    context = {}
    if request.POST:
        form = ShowTodolistForm(request)
        Todo = Todolist.objects.filter(id=id).first()
        Todo.data = request.POST['data']
        Todo.save()
        return redirect('/todolist')
    else:
        if len(todolist.objects.filter(id=id)) > 0:
            todo = todolist.objects.filter(id=id).first()
            context = {
                'header': "Show note page header",
                'id': id,
                'title': todo.name
            }
            form = ShowTodolistForm({'data': todolist.data})
            context['form'] = form
        else:
            context['error'] = True
        return render(request, "todos/edit_todolist.html", context)