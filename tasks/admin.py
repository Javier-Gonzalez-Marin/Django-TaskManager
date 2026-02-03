from django.contrib import admin
from .models import Project, Task

# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'deadline', 'created_at')
    list_filter = ('deadline', 'owner')
    search_fields = ('title',)
    filter_horizontal = ('collaborators',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assigned_to')
    list_filter = ('status', 'priority')
    search_fields = ('title',)
