from django.contrib import admin
from .models import Task, Photo
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title','priority', 'is_completed', 'due_date', 'completed_by']
    list_editable = ['due_date']
    list_filter = ('priority', 'due_date', 'is_completed')
    search_fields = ('title', 'description', 'completed_by__username')

admin.site.register(Task, TaskAdmin)
admin.site.register(Photo)