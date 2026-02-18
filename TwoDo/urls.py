"""
URL configuration for TwoDo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

import ai.views as ai_views
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/create/', views.create_task, name='create'),
    path('tasks/<int:task_id>/edit/', views.edit, name='edit'),
    path('tasks/<int:task_id>/delete/', views.delete, name='delete'),
    path('tasks/<int:task_id>/toggle/', views.toggle_status, name='toggle_status'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path(
"password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="user/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="user/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="user/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="user/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("profile/", lambda request: redirect('profile', username=request.user.username), name="my_profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path("profile/edit/change-password/", views.change_password, name="change_password"),
    path('lists/', views.lists, name='lists'),
    path('lists/create/', views.create_list, name='create_list'),
    path('lists/<int:list_id>/', views.list_detail, name='list_detail'),
    path("friends/", views.friends_page, name="friends_page"),
    path("friends/send/<int:user_id>/", views.send_friend_request, name="send_friend_request"),
    path("friends/accept/<int:request_id>/", views.accept_friend_request, name="accept_friend_request"),
    path("lists/<int:list_id>/share/", views.share_list, name="share_list"),
    path("friends/remove/<int:user_id>/", views.remove_friend, name="remove_friend"),
    path("friends/cancel/<int:request_id>/",views.cancel_friend_request,name="cancel_friend_request"),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path("admin-panel/toggle-mode/", views.toggle_admin_mode, name="toggle_admin_mode"),
    path(
        "admin-panel/delete-user/<int:user_id>/",
        views.delete_user,
        name="delete_user",
    ),
    path('admin-panel/make-admin/<int:user_id>/', views.make_admin, name="make_admin"),
    path('ai-assistant/', ai_views.assistant_page, name='ai_assistant_page'),
    path('ai-assistant/api/', ai_views.assistant_api, name="ai_assistant_api"),
]
