# Role_based_Access/admin.py
from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_username', 'email', 'department')
    search_fields = ('name', 'email', 'department', 'user__username')
    list_filter = ('department',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Clear existing groups
        obj.user.groups.clear()
        # Assign to new group based on department
        group_name = f"{obj.department}_group"
        group, created = Group.objects.get_or_create(name=group_name)
        obj.user.groups.add(group)

admin.site.register(Employee, EmployeeAdmin)