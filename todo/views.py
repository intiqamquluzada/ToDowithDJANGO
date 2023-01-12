from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo, User
from django.db.models import Case, When, Value, CharField, Q
from django.contrib import messages
from .forms import TodoForm


def list_view(request):
    user = request.user
    todo_list = Todo.objects.filter(user=user).annotate(

        status_value=Case(
            When(status="Completed", then=Value('checked')),
            default=Value(""),
            output_field=CharField()
        )

    ).order_by('-created_at')

    status = request.GET.get('status', None)
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    filter_ = Q()

    if status and status != "All":
        filter_.add(Q(status=status), Q.AND)
    if start_date:
        filter_.add(Q(deadline__gte=start_date), Q.AND)
    if end_date:
        filter_.add(Q(deadline__lt=end_date), Q.AND)

    todo_list = todo_list.filter(filter_)

    context = {
        'todo_list': todo_list
    }
    return render(request, 'list.html', context)


def delete_view(request, slug):
    todo = get_object_or_404(Todo, slug=slug)
    messages.success(request, f"{todo.task_name} is deleted !")
    todo.delete()
    return redirect("todo:list")


def create_view(request):
    context = {}
    form = TodoForm()

    if request.method == 'POST':
        form = TodoForm(request.POST or None)
        if form.is_valid():
            data = form.save()
            messages.success(request, f"\"{data.task_name}\"  is successfully created!")
            return redirect("todo:list")

    context['form'] = form
    return render(request, 'create.html', context)


def update_view(request, slug):

    todo = get_object_or_404(Todo, slug=slug)
    context = {}
    form = TodoForm(instance=todo)
    if request.method == "POST":
        form = TodoForm(request.POST or None, instance=todo)
        if form.is_valid():
            obj = form.save()
            if "check" in request.POST:
                obj.status = "Completed"
                obj.save()
            return redirect("todo:list")
    context['form'] = form
    return render(request, 'create.html', context)
