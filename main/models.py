from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class TaskList(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lists"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    task_list = models.ForeignKey(
        TaskList,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,
        blank=True
    )

class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_requests"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_requests"
    )
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver}"

    @staticmethod
    def get_friends(user):
        return User.objects.filter(
            Q(sent_requests__receiver=user, sent_requests__accepted=True) |
            Q(received_requests__sender=user, received_requests__accepted=True)
        )