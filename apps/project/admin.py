from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from rangefilter.filter import DateRangeFilter

from .models import Project, Task, Entry


class EntryResource(resources.ModelResource):
    class Meta:
        model = Entry
        fields = ('task__title', 'project__title', 'team__title', 'minutes', 'created_by__username', 'created_at')
        export_order = ('task__title', 'project__title', 'team__title', 'created_by__username', 'created_at', 'minutes')


class TaskResource(resources.ModelResource):
    total_minutes = Field(attribute='registered_time')

    class Meta:
        model = Task
        fields = (
            'title', 'project__title', 'team__title', 'created_by__username', 'created_at', 'status')
        export_order = (
            'title', 'project__title', 'team__title', 'created_by__username', 'created_at', 'status')


@admin.register(Entry)
class EntryAdmin(ImportExportModelAdmin):
    list_display = ['project', 'task', 'minutes', 'created_by', 'created_at']
    list_filter = [('created_at', DateRangeFilter), 'created_by__username', 'project__title', 'task__title']
    search_fields = ['project__title', 'task__title', 'created_by__username']
    resource_class = EntryResource


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    date_hierarchy = 'create_at'
    list_display = ['title', 'team', 'created_by', 'registered_time', 'num_tasks_todo', 'create_at', 'status']
    list_filter = [('create_at', DateRangeFilter), 'status', 'title', 'team', 'created_by']
    search_fields = ['title', 'team__title', 'created_by__username']
    save_as = True


@admin.register(Task)
class TaskAdmin(ImportExportModelAdmin):
    list_display = ['title', 'project', 'team', 'created_by', 'registered_time', 'status']
    list_filter = [('created_at', DateRangeFilter), 'status', 'title', 'team', 'project', 'created_by']
    search_fields = ['title', 'team__title', 'project__title', 'created_by__username']
    resource_class = TaskResource
    # save_as = True

# admin.site.register(Project)
# admin.site.register(Task)
# admin.site.register(Entry)
