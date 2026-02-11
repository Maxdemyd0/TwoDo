from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from main.models import Task
from django.contrib.auth.forms import UserCreationForm

@login_required
def create_task(request):
    if request.method == "POST":
        post_data = request.POST
        Task.objects.create(
            name=post_data["name"],
            description=request.POST.get("description", ""),
            status=False,
            user=request.user
        )
        return redirect("tasks")
    return render(request, "create.html")

@login_required
def task_list(request):
    filter_status = request.GET.get("filter")

    tasks = request.user.tasks.all()

    if filter_status == "active":
        tasks = tasks.filter(status=False)
    elif filter_status == "completed":
        tasks = tasks.filter(status=True)

    tasks = tasks.order_by("status", "-id")

    return render(request, "tasks.html", {
        "tasks": tasks,
        "current_filter": filter_status
    })

@login_required
def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.name = request.POST["name"]
        task.description = request.POST.get("description", "")
        task.save()
        return redirect("tasks")

    return render(request, "edit.html", {"task": task})

@login_required
def delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.delete()
        return redirect("tasks")

    return redirect("tasks")

@login_required
def toggle_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.status = "status" in request.POST
        task.save()

    return redirect("tasks")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("tasks")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def home(request: HttpRequest):
    return render(request, "home.html")