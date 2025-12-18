

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class TaskGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TaskItem(models.Model):
    group = models.ForeignKey(TaskGroup, on_delete=models.CASCADE, related_name='tasks')
    description = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description