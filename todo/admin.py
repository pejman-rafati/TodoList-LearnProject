from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models import QuerySet, Subquery, OuterRef
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models
from .models import User


# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'type', 'task_quantity', 'list_quantity')
    list_editable = ['type']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith', 'email__istartswith']
    list_per_page = 10

    @admin.display(ordering='task_quantity')
    def task_quantity(self, user):
        url = reverse('admin:todo_task_changelist') + '?' + urlencode({'user__id': str(user.id)})
        return format_html('<a href="{}">{}</a>', url, user.task_quantity)

    @admin.display(ordering='list_quantity')
    def list_quantity(self, user):
        url = reverse('admin:todo_list_changelist') + '?' + urlencode({'user__id': str(user.id)})
        return format_html('<a href="{}">{}</a>', url, user.list_quantity)

    # this get_queryset shows wrong the value of the count of lists
    # def get_queryset(self, request):
    #     return super().get_queryset(request).annotate(task_quantity=Count('task'), list_quantity=Count('list'))

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            task_quantity=Subquery(
                User.objects.filter(id=OuterRef('id'))
                .annotate(task_count=Count('task'))
                .values('task_count')[:1]
            ),
            list_quantity=Subquery(
                User.objects.filter(id=OuterRef('id'))
                .annotate(list_count=Count('list'))
                .values('list_count')[:1]
            )
        )


class ReminderInline(admin.TabularInline):
    model = models.Reminder
    extra = 0


class TaskInline(admin.TabularInline):
    model = models.Task
    extra = 0
    search_fields = ['title', 'description']


@admin.register(models.Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('alarm_on', 'task', 'user')
    list_select_related = ['task', 'user']
    list_filter = ['task', 'user', 'alarm_on']


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'tasks_number')
    ordering = ['user', 'task']
    list_filter = ['user']
    search_fields = ['title']
    inlines = [TaskInline]

    @admin.display(ordering='tasks_number')
    def tasks_number(self, list):
        url = reverse('admin:todo_task_changelist') + '?' + urlencode({'user__id': str(list.user.id)})
        return format_html('<a href="{}">{}</a>', url, list.tasks_number)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(tasks_number=Count('task'))


class TaskStatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('done', 'Done'),
            ('not_done', 'Not Done'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'done':
            return queryset.filter(status=True)
        elif self.value() == 'not_done':
            return queryset.filter(status=False)


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ['title']
    actions = ['change_to_done', 'change_to_not_done']
    list_display = ['title', 'status', 'priority', 'list', 'created_at', 'reminders', 'user']
    exclude = ['status']
    preserve_filters = {'list': 'Null'}
    autocomplete_fields = ['user']
    ordering = ['-created_at']
    list_editable = ['priority', 'list', 'status']
    list_select_related = ['list', 'user']
    list_filter = ['user', 'list', 'start_time', TaskStatusFilter]
    inlines = [ReminderInline]
    list_per_page = 10
    fieldsets = (
        (None, {'fields': ('title', 'description', 'priority', 'list', 'user')}),
        ('Start and End Time', {'fields': ('start_time', 'end_time'), 'classes': ('collapse',)}),
    )

    @admin.display(ordering='reminders')
    def reminders(self, task):
        if task.reminders == 0:
            return 'Null'
        else:
            url = reverse('admin:todo_reminder_changelist') + '?' + urlencode({'task__id': str(task.id)})
            return format_html('<a href="{}">{}</a>', url, task.reminders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(reminders=Count('reminder'))

    @admin.action(description='Change status to "Done"')
    def change_to_done(self, request, queryset: QuerySet):
        if queryset.filter(status=False).exists():
            updated_count = queryset.update(status=True)
            self.message_user(
                request,
                f'{updated_count} task status has been updated to "Done".'
            )
        elif queryset.filter(status=True).exists():
            self.message_user(
                request,
                f'This task is already "Done".',
                messages.ERROR
            )

    @admin.action(description='Change status to "Not Done"')
    def change_to_not_done(self, request, queryset):
        if queryset.filter(status=True).exists():
            updated_count = queryset.update(status=False)
            self.message_user(
                request,
                f'{updated_count} task status has been updated to "Not Done".'
            )
        elif queryset.filter(status=False).exists():
            self.message_user(
                request,
                f'This task is already "Not Done".',
                messages.ERROR
            )
