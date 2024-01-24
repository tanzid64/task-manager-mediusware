from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
    list_display_links = ['username', 'first_name', 'last_name']
    list_editable = ['is_active',]
admin.site.register(User, UserAdmin)