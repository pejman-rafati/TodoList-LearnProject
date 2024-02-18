from datetime import datetime
from django.utils import timezone
from django.core.validators import validate_email

from django.core.exceptions import ValidationError
from django.db import models


class User(models.Model):
    USER_TYPE_DEFAULT = 'F'
    USER_TYPE_CHOICES = {
        ('F', 'Free'),
        ('P', 'Pro'),
        ('A', 'Admin')
    }
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[validate_email])
    phone = models.IntegerField(unique=True)
    type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=USER_TYPE_DEFAULT)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class List(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'user')

    def __str__(self):
        return self.title


def validate_start_end_time(value):
    today = timezone.now().date()
    if value.date() < today:
        raise ValidationError('Start time cannot be earlier than today.')


class Task(models.Model):
    PRIORITY_CHOICES_DEFAULT = "L"
    PRIORITY_CHOICES = {
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High')
    }
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True, validators=[validate_start_end_time])
    end_time = models.DateTimeField(blank=True, null=True, validators=[validate_start_end_time])
    priority = models.CharField(
        max_length=1, choices=PRIORITY_CHOICES, default=PRIORITY_CHOICES_DEFAULT)
    status = models.BooleanField(default='False')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    list = models.ForeignKey(
        List, on_delete=models.SET_NULL, null=True, default='null', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Reminder(models.Model):
    alarm_on = models.DateTimeField(validators=[validate_start_end_time])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f'reminder for: {self.task.title}'
