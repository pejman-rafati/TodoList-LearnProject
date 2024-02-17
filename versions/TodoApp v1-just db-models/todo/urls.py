from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.simple_index)
]
