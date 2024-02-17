from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Reminder)


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'list']
    ordering = ['title']
    list_editable = ['status', 'priority', 'list']
    list_per_page = 10


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_editable = ['email']
    list_per_page = 10
