from django.contrib import admin
from .models import Task, Photo
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title','priority', 'is_completed', 'completed_by']
    list_editable = ['priority',]
admin.site.register(Task, TaskAdmin)
admin.site.register(Photo)