from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from main.forms import RegisterForm, TaskForm, EditProfileForm
from main.models import Task, TaskList, FriendRequest
from typing import Any
from django.db import transaction

from main.utils import is_admin_mode


@login_required
def create_task(request):
    selected_list_id = request.GET.get("list")

    if request.method == "POST":
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("tasks")
    else:
        initial_data = {}

        if selected_list_id:
            initial_data["task_list"] = selected_list_id

        form = TaskForm(
            user=request.user,
            initial=initial_data
        )

    return render(request, "tasks/create.html", {"form": form})


@login_required
def tasks(request):
    current_filter = request.GET.get("filter", "")

    if is_admin_mode(request):
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(user=request.user)

    if current_filter == "active":
        tasks = tasks.filter(status=False)
    elif current_filter == "completed":
        tasks = tasks.filter(status=True)

    return render(request, "tasks/tasks.html", {
        "tasks": tasks,
        "current_filter": current_filter,
    })


@login_required
def edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.user != request.user and not is_admin_mode(request):
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("tasks")

    else:
        form = TaskForm(instance=task, user=request.user)

    return render(request, "tasks/edit.html", {"form": form})

@login_required
def delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.user != request.user and not is_admin_mode(request):
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        task.delete()
        return redirect("tasks")

    return redirect("tasks")

@login_required
def toggle_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.user != request.user and not is_admin_mode(request):
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        task.status = "status" in request.POST
        task.save()

    return redirect("tasks")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                TaskList.objects.create(
                    name=f"{user.username}'s Tasks",
                    owner=user
                )
            login(request, user)
            return redirect("tasks")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = RegisterForm()

    return render(request, "user/register.html", {"form": form})

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

    return render(request, "user/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def home(request: HttpRequest):
    return render(request, "home.html")

@login_required
def profile(request, username):
    user_obj = get_object_or_404(User, username=username)

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

    return render(request, "user/profile.html", context)

@login_required
def create_list(request):
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            TaskList.objects.create(
                name=name,
                owner=request.user
            )
            return redirect("lists")

    return render(request, "lists/create_list.html")

@login_required
def lists(request):

    if is_admin_mode(request):
        owned_lists = TaskList.objects.all()
        shared_lists = TaskList.objects.none()  # avoid duplicates
    else:
        owned_lists = TaskList.objects.filter(owner=request.user)
        shared_lists = TaskList.objects.filter(shared_with=request.user)

    return render(request, "lists/lists.html", {
        "owned_lists": owned_lists,
        "shared_lists": shared_lists,
    })

@login_required
def list_detail(request, list_id):

    task_list = get_object_or_404(TaskList, id=list_id)

    # Permission check
    if (
        task_list.owner != request.user
        and request.user not in task_list.shared_with.all()
        and not is_admin_mode(request)
    ):
        return HttpResponseForbidden("You do not have permission to view this list.")

    tasks = task_list.tasks.all()

    return render(request, "lists/list_view.html", {
        "list": task_list,
        "tasks": tasks,
        "is_admin_mode": is_admin_mode(request),
    })

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "user/edit_profile.html", {
        "form": form
    })

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()

            # Log the user out after password change
            logout(request)

            messages.success(
                request,
                "Your password was changed successfully. Please log in again."
            )

            return redirect("login")  # Make sure you have a login URL name
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "user/change_password.html", {
        "form": form
    })


@login_required
def friends_page(request):
    tab = request.GET.get("tab", "friends")

    context: dict[str, Any] = {"tab": tab}

    # FRIENDS TAB
    if tab == "friends":
        friends = FriendRequest.get_friends(request.user)
        context["friends"] = friends

    # SEARCH TAB
    elif tab == "search":
        query = request.GET.get("q")
        users = []

        if query:
            users = User.objects.filter(
                username__icontains=query
            ).exclude(id=request.user.id)

        friends = FriendRequest.get_friends(request.user)

        sent_requests = FriendRequest.objects.filter(
            sender=request.user,
            accepted=False
        )

        received_requests = FriendRequest.objects.filter(
            receiver=request.user,
            accepted=False
        )

        users_with_status = []

        for user in users:
            if user in friends:
                status = "friends"
                request_id = None

            elif sent_requests.filter(receiver=user).exists():
                status = "sent"
                request_id = None

            elif received_requests.filter(sender=user).exists():
                status = "received"
                request_id = received_requests.get(sender=user).id

            else:
                status = "none"
                request_id = None

            users_with_status.append((user, status, request_id))

        context["users_with_status"] = users_with_status

    # REQUESTS TAB
    elif tab == "requests":
        requests = FriendRequest.objects.filter(
            receiver=request.user,
            accepted=False
        )
        context["requests"] = requests

    #SENT TAB
    elif tab == "sent":
        sent_requests = FriendRequest.objects.filter(
            sender=request.user,
            accepted=False
        )
        context["sent_requests"] = sent_requests

    return render(request, "friends.html", context)

@login_required
def send_friend_request(request, user_id):
    receiver = User.objects.get(id=user_id)

    if receiver != request.user:
        FriendRequest.objects.get_or_create(
            sender=request.user,
            receiver=receiver,
            accepted=False
        )

    return redirect(f"{reverse('friends_page')}?tab=search")

@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)

    if friend_request.receiver == request.user:
        friend_request.accepted = True
        friend_request.save()

    return redirect("profile", username=request.user.username)

@login_required
def cancel_friend_request(request, request_id):
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        sender=request.user,
        accepted=False
    )

    friend_request.delete()

    return redirect(f"{reverse('friends_page')}?tab=sent")

@login_required
def share_list(request, list_id):
    task_list = get_object_or_404(TaskList, id=list_id)

    if task_list.owner != request.user and not is_admin_mode(request):
        return redirect("lists")

    friends = FriendRequest.get_friends(request.user) # adjust to your friend model

    if request.method == "POST":
        friend_id = request.POST.get("friend_id")
        friend = get_object_or_404(User, id=friend_id)
        task_list.shared_with.add(friend)
        return redirect("lists")

    return render(request, "lists/share_list.html", {
        "task_list": task_list,
        "friends": friends
    })

@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)

    friendship = FriendRequest.objects.filter(
        Q(sender=request.user, receiver=friend, accepted=True) |
        Q(sender=friend, receiver=request.user, accepted=True)
    ).first()

    if friendship:
        friendship.delete()

    return redirect(f"{reverse('friends_page')}?tab=friends")

@login_required
def admin_panel(request):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden("Not allowed")

    tab = request.GET.get("tab", "users")

    users = User.objects.all()

    total_users = users.count()
    total_admins = users.filter(is_staff=True).count()

    return render(request, "admin_panel.html", {
        "tab": tab,
        "users": users,
        "total_users": total_users,
        "total_admins": total_admins,
    })

@login_required
def delete_user(request, user_id):
    if not is_admin_mode(request):
        return HttpResponseForbidden("Not allowed")

    user = get_object_or_404(User, id=user_id)

    # Prevent deleting yourself
    if user == request.user:
        return HttpResponseForbidden("You cannot delete yourself.")

    # Prevent deleting superusers unless you are superuser
    if user.is_superuser and not request.user.is_superuser:
        return HttpResponseForbidden("Only superusers can delete another superuser.")

    # Prevent deleting admins unless you are superuser
    if user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden("Only superusers can delete another admin.")

    return redirect("admin_panel")

@login_required
def make_admin(request, user_id):
    if not is_admin_mode(request):
        return HttpResponseForbidden("Not allowed")

    user = get_object_or_404(User, id=user_id)
    user.is_staff = True
    user.save()

    return redirect("admin_panel")

@login_required
def toggle_admin_mode(request):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden("Admins only.")

    current = request.session.get("admin_mode", False)
    request.session["admin_mode"] = not current

    return redirect(request.META.get("HTTP_REFERER", "home"))