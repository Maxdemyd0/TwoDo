from django import forms as django_forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from main.models import Task, TaskList


class RegisterForm(UserCreationForm):
    email = django_forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class TaskForm(django_forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "status", "task_list"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["task_list"].queryset = TaskList.objects.filter(user=user)

class EditProfileForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]