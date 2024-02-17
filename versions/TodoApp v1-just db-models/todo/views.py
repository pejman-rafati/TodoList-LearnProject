from django.shortcuts import render
from django.http import HttpResponse


def simple_index(request):
    return render(request, 'index.html', {'name': 'pejman'})
