from django.db import models

class Task(models.Model):
    from django.contrib.auth.models import User
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    def __str__(self):
        return self.name
