from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from main.forms import RegisterForm, TaskForm
from main.models import Task, TaskList


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("tasks")

    else:
        default_list = request.user.lists.first()

        form = TaskForm(
            user=request.user,
            initial={"task_list": default_list}
        )

    return render(request, "create.html", {"form": form})


@login_required
def tasks(request):
    user_lists = request.user.lists.all()

    # Get selected list and filter from GET params
    selected_list_id = request.GET.get("list", "")
    current_filter = request.GET.get("filter", "")

    tasks_qs = Task.objects.filter(user=request.user)

    # Filter by list
    if selected_list_id and request.user.lists.filter(id=selected_list_id).exists():
        tasks_qs = tasks_qs.filter(task_list_id=selected_list_id)

    # Filter by status
    if current_filter == "active":
        tasks_qs = tasks_qs.filter(status=False)
    elif current_filter == "completed":
        tasks_qs = tasks_qs.filter(status=True)

    tasks_qs = tasks_qs.order_by("status")

    context = {
        "tasks": tasks_qs,
        "lists": user_lists,
        "selected_list_id": selected_list_id,
        "current_filter": current_filter,  # <-- send to template
    }

    return render(request, "tasks.html", context)


@login_required
def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("tasks")

    else:
        form = TaskForm(instance=task, user=request.user)

    return render(request, "edit.html", {"form": form})

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
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            TaskList.objects.create(
                name="My Tasks",
                user=user
            )
            login(request, user)
            return redirect("tasks")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

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

@login_required
def profile(request):
    return profile_detail(request, request.user.id)

@login_required
def profile_detail(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    tasks = Task.objects.filter(user=user_obj)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status=True).count()
    incomplete_tasks = tasks.filter(status=False).count()

    context = {
        "user_obj": user_obj,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "incomplete_tasks": incomplete_tasks,
        "is_self": request.user == user_obj,
    }

    return render(request, "profile.html", context)

@login_required
def create_list(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            TaskList.objects.create(
                name=name,
                user=request.user
            )
            return redirect("lists")

    return render(request, "create_list.html")

@login_required
def lists(request):
    user_lists = request.user.lists.all()
    return render(request, "lists.html", {"lists": user_lists})

@login_required
def list_detail(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id, user=request.user)
    tasks = task_list.tasks.all()

    return render(request, "tasks.html", {
        "tasks": tasks,
        "current_list": task_list
    })