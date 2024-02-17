from datetime import datetime

from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class List(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'user')

    def __str__(self):
        return self.title


class Task(models.Model):
    PRIORITY_CHOICES_DEFAULT = "L"
    PRIORITY_CHOICES = {
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High')
    }
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    priority = models.CharField(
        max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_CHOICES_DEFAULT)
    status = models.BooleanField(default='False')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    list = models.ForeignKey(
        List, on_delete=models.SET_NULL, null=True, default='null')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Reminder(models.Model):
    alarm_on = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'reminder for: {self.task.title}'
