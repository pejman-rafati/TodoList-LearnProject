from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse
from todo.models import Task, User


def simple_index(request):
    todos = Task.objects.values('id', 'title', 'user__first_name')

    return render(request, 'index2.html', {'todos': list(todos)})
