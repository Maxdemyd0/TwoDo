from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
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
        return redirect("task_list")
    return render(request, "create.html")

@login_required
def task_list(request):
    tasks = request.user.tasks.all()
    return render(request, "tasks.html", {"tasks": tasks})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
        else:
            print(form.errors)
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
            return redirect("task_list")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def home(request: HttpRequest):
    return render(request, "home.html")